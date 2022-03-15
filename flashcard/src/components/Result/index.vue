<template>
    <div v-if="current_response">
        <h1 class="text-center fs-4 mt-5">Congratulations! You have completed the deck!</h1>
        <div class="progress mt-5 w-75 mx-auto bg-danger" style="height:25px;">
            <div class="progress-bar bg-success" :style="'width:'+current_response.score + '%'" id="progressBar" role="progressbar">
                {{current_response.score}}%
            </div>
        </div>
        <div class="mx-auto d-block w-75">
            <div class="avg_time mt-4">
                <h3 class="fs-5">Averge time :- {{ get_time(current_response.avg_time) }} sec</h3>
            </div>
            <div class="completed_at">
                <h3 class="fs-5">Completed At :- {{ new Date(current_response.completed_at).toLocaleString('en-In') }}</h3>
            </div>
            <div class="question_type">
                <table class="table table-hover">
                    <thead>
                        <tr class="text-center">
                            <th scope="col">#</th>
                            <th scope="col">Question</th>
                            <th scope="col">Correct Answer</th>
                            <th scope="col">Your Answer</th>
                            <th scope="col">Time taken</th>
                            <th scope="col">Difficulty</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item,index in current_response.cards" :key="index" 
                            :class="item.difficulty"  class="text-center">
                            <td>{{ index + 1}}</td>
                            <td>{{ item.card.front }}</td>
                            <td>{{ item.correct_option }}</td>
                            <td>{{ item.selected_option }}</td>
                            <td>{{ get_time(item.time)}} secs</td>
                            <td>{{ item.difficulty }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <router-link :to="{name:'Home'}" class="btn btn-primary mx-auto mt-5 d-block w-50">
                Go Home
            </router-link>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "DeckTestResult",
    data() {
        return {
        };
    },
    computed: {
        ...mapGetters(["current_response"])
    },
    methods: {
        ...mapActions([
            "set_current_response", "set_loader"
        ]),
        get_time(time){
            if(time > 0){
                var minutes = Math.floor(time / 60000);
                var seconds = ((time % 60000) / 1000).toFixed(0);
                return (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00"
        }
    },
    watch:{
    },
    created(){
        this.set_loader(true);
        this.set_current_response(this.$route.params.response_id).then(()=>{
            this.set_loader(false);
        })
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

.question_type tr{
    font-size: 1.1rem;
}
</style>