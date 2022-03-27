<template>
    <div v-if="current_deck" id="review">
        <div class="container-sm w-75 bg-light p-2 pb-5 mt-5">
            <div v-if="card">
                <h6 class="time fs-5 text-center d-block ms-auto"></h6>
                <div class="question_card" :class="response.answer ? (response.isQuestionCorrect ? 'bg-success' : 'bg-danger') : ''">
                    <h1 class="text-center">
                        <span v-if="response.answer">{{response.answer}}</span>
                        <span v-else>{{card.front}}</span>
                    </h1>
                    <span class="timer">{{ timer }} secs</span>
                </div>
                <ul class="list-group">
                    <li v-for="option,index in card_options" :key="index" class="list-group-item">
                        <input class="form-check-input" type="radio" :name="'_'+card.id" v-model="selected_option"
                            :value="option.trim()" :id="option + '_' + index" :disabled="response.answer">
                        <label class="form-check-label" :for="option + '_' + index">
                            {{option}}
                        </label>
                    </li>
                </ul>
                <button v-if="!response.answer" @click="submitAnswer" :disabled="submitLoader"
                    class="btn btn-primary w-25 mx-auto mt-3 d-block">
                    <div v-if="submitLoader" class="spinner-border spinner-border-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span v-else id="submit_text">
                        Show answer
                    </span>
                </button>
                <form v-if="response.isQuestionDone" @submit.prevent="nextQuestion">
                    <input type="text" name="next" id="next" value="{{card.next}}" hidden>
                    <input type="text" name="response_id" id="response_id" hidden>
                    <div class="sort_options">
                        <h5 class="d-block w-100 text-center">
                            Difficulty Level
                        </h5>
                        <div class="sorts mx-auto w-100">
                            <div class="option">
                                <input type="radio" name="difficulty" id="easy" value="1" v-model="difficulty" hidden />
                                <label for="easy" class="shadow">
                                    <span>Easy</span>
                                </label>
                            </div>
                            <div class="option">
                                <input type="radio" name="difficulty" id="modarate" value="2" v-model="difficulty" checked hidden />
                                <label for="modarate" class="shadow">
                                    <span>Moderate</span>
                                </label>
                            </div>
                            <div class="option">
                                <input type="radio" name="difficulty" id="hard" value="3" v-model="difficulty" hidden />
                                <label for="hard" class="shadow">
                                    <span>Hard</span>
                                </label>
                            </div>
                            <button type="submit" :disabled="submitLoader"
                                class="btn btn-primary w-25 mx-auto mt-3 d-block">
                                <div v-if="submitLoader" class="spinner-border spinner-border-sm" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <span v-else id="submit_text">
                                    Next 
                                    <i class="fas fa-chevron-right"></i>
                                </span>
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapActions, mapGetters } from 'vuex';
import {REMOTE_URL, get_token} from '@/constants/constant.js';
var lodash = require('lodash')
export default {
    name: "DeckTest",
    data() {
        return {
            isFinish:false,
            card:null,
            submitLoader:false,
            current_question:0,
            selected_option:null,
            difficulty:null,
            response:{
                isQuestionDone:false,
                isQuestionCorrect:false,
                answer:null,
                response_id:null,
            },
            time:0,
            current_time:0,
            interval:null,
            final_response:null,
            previous_card:null,
            cards:null,
        };
    },
    computed: {
        ...mapGetters(["current_deck", "user", "loader"]),
        card_options(){
            let options = []
            if(this.card.options){
                options = this.card.options.split(',').filter(a => a !== undefined || a !== null)
                options = lodash.shuffle(options)
            }
            return options
        },
        timer(){
            let millis = this.current_time - this.time;
            if(millis > 0){
                var minutes = Math.floor(millis / 60000);
                var seconds = ((millis % 60000) / 1000).toFixed(0);
                return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00";
        }
    },
    methods: {
        ...mapActions([
            "set_current_deck", "set_loader", "set_loader_message", 
            "set_toast_message", "set_error_message", "set_user"
        ]),
        submitAnswer() {
            console.log(this.selected_option);

            if(!this.selected_option){
                return false
            }

            this.submitLoader=true;
            if(this.interval)
                clearInterval(this.interval)
            
            let data = {
                card_id:this.card.id,
                time:new Date() - this.time,
                answer:this.selected_option
            }

            let auth_token= get_token()
            axios.post(REMOTE_URL + "review", data,  {
                headers:{
                    "Auth-Token":auth_token,
                    "Content-type":"application/json"
                }
            }).then(res=>{
                if(res.data.status){
                    this.response.isQuestionDone =true;
                    this.response.answer = res.data.answer;
                    this.response.isQuestionCorrect = res.data.correct;
                    this.selected_option = null;
                    this.final_response = res.data.response;
                    this.previous_card = res.data.card;
                }
                this.submitLoader=false
            }).catch((err)=>{
                this.response.isQuestionDone =false;
                this.submitLoader=false;
                this.set_error_message(err)
            })
        },
        nextQuestion(){

            if(!this.difficulty)
                this.difficulty = "2"
            
            if(!this.previous_card){
                return false
            }

            this.submitLoader=true;
            
            let data = {
                difficulty:this.difficulty,
            }

            let auth_token= get_token()
            axios.put(REMOTE_URL + "review/" + this.previous_card.id, data,  {
                headers:{
                    "Auth-Token":auth_token,
                    "Content-type":"application/json"
                }
            }).then(res=>{
                if(res.data.status){
                    this.current_question++;
                }
                this.submitLoader=false
            }).catch((err)=>{
                this.submitLoader=false;
                this.set_error_message(err)
            })
        },
        user_or_deck_changed(){
            if(this.user && this.current_deck){
                this.cards = this.current_deck.cards;
                let responses = this.user.response || []
                this.final_response = responses.find(a => a.deck_id === this.current_deck.id)
                if(this.final_response && this.final_response.cards.length > 0){
                    this.cards = this.current_deck.cards.filter(a => !this.final_response.cards.some(b => b.card_id === a.id ))
                }
            }
            this.current_question = 0;
            
        },
        cards_or_question_changed(){
            if(this.current_deck && this.cards){
                console.log(this.cards);
                if(this.current_question >= this.cards.length){
                    this.isFinish = true
                }else{
                    this.card = this.cards[this.current_question]
                }
            }
        }
    },
    watch:{
        card(){
            this.time = new Date();
            this.interval = setInterval(() => {
                this.current_time = new Date()
            }, 1000);
            this.response.isQuestionDone =false;
            this.response.answer = null;
            this.response.isQuestionCorrect = false;
            this.selected_option = null;
            this.difficulty = null;
        },
        user(){
            console.log(this.user);
            this.user_or_deck_changed()
        },
        current_deck(){
            this.user_or_deck_changed()
        },
        current_question:{
            handler(){
                this.cards_or_question_changed()
            },
            immediate:true
        },
        cards(){
            this.cards_or_question_changed()
        },
        isFinish(val){
            if(val && this.final_response){
                this.$router.push({name:"Result", params:{response_id:this.final_response.id}})
            }
        }
    },
    created(){
        this.set_user({isAll:true, isLogout:false});
        this.set_loader(true);
        this.set_current_deck(this.$route.params.deck_id).then(()=>{
            this.set_loader(false);
        })
    },
    mounted(){
    },
    beforeUnmount(){
        if(this.interval)
            clearInterval(this.interval)
    }
};
</script>

<style scoped>

.sort_options{
    margin: 45px 0 25px;
    position: relative;
    display: block;
}
.sorts{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    column-gap: 15px;
    row-gap: 15px;
    max-width: max-content;
}
.sort_title{
    font-size: 1.2rem;
    font-family: var(--font-medium);
    background: var(--buttonColor);
    color: var(--white);
    padding: 5px 15px;
    min-width: 170px;
    display: flex;
    align-items: center;
    border-radius: 150px;
}
.sort_title i{
    margin:0 0 0 auto;
}
.option label{
    font-size: 1.1rem;
    font-family: var(--font-medium);
    color: var(--active-color);
    background: var(--white);
    padding: 5px 25px;
    min-width: 150px;
    display: flex;
    align-items: center;
    border-radius: 150px;
    cursor: pointer;
    text-transform: capitalize;
}

.sort_options input[type="radio"]:checked + label{
    background: var(--buttonColor);
    color: var(--white);
}

[type="radio"] + label{
    cursor: pointer;
}
.form-check-label{
    width:90%;
}

.question_card{
    height: 100%;
    min-height: 150px;
    border-radius: 15px;
    background: var(--backgroundColor);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    transform-style: preserve-3d;
    perspective: 500px;
    transition: .9s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    margin: 25px auto;
    position: relative;
}
.question_card h1{
    font-family: var(--font-medium);
    font-size: 1.7rem;
    transform-style: preserve-3d;
    perspective: 500px;
    position: unset;
}
.timer{
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 1rem;
    font-family: var(--font-medium);
}
#answer{
    display: block;
    width: 100%;
    text-align: center;
}
.show-answer{
    color: var(--white);
    transform: rotateY(180deg);
}

.show-answer h1{
    transform: rotateY(180deg);
}

.question_type ul{
    list-style-type: none;
    display: flex;
    justify-content: space-evenly;
    margin-top: 50px;

}
.question_type li{
    font-size: 1.4rem;
}
.question_type li::before{
    content: "";
    width:35px;
    height:35px;
    position: relative;
    display: inline-block;
    vertical-align: middle;
}

.bg-success, .bg-danger{
    color: var(--white);
}
.Easy::before{
    background: seagreen;
}
.Moderate::before{
    background: yellowgreen;
}
.Hard::before{
    background: tomato;
}

@media screen and (max-width:600px) {
    .container-sm {
        width: 95% !important;
    }
    #review .btn.w-25{
        width: 100% !important;
    }
}
</style>