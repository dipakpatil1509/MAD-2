<template>
    <div id="review">
    <div class="container-sm w-75 bg-light p-2 pb-5 mt-5">

        <div v-if="isFinish">
            <h1 class="text-center fs-4 mt-5">Congratulations! You have completed the deck!</h1>
            <div class="progress mt-5 w-75 mx-auto bg-danger" style="height:25px;">
                <div class="progress-bar bg-success" :style="'width:'+final.score" id="progressBar" role="progressbar">
                    {{final.score}}%
                </div>
            </div>
            <div class="mx-auto d-block w-75">
                <div class="avg_time mt-4">
                    <h3 class="fs-5">Averge time :- {{ final.avg_time }} sec</h3>
                </div>
                <div class="completed_at">
                    <h3 class="fs-5">Completed At :- {{ final.completed_at }}</h3>
                </div>
                <div class="question_type">
                    <ul>
                        <li v-for="item,index in final_cards" :key="index" 
                            :class="item.difficulty.name">
                            {{ item.difficulty.name }} - {{ item[1] }}
                        </li>
                    </ul>
                </div>
                <router-link :to="{name:'Home'}" class="btn btn-primary mx-auto mt-5 d-block w-50">
                    Go Home
                </router-link>
            </div>
        </div>
        <div v-else>
            <h6 class="time fs-5 text-center d-block ms-auto"></h6>
            <div class="question_card">
                <h1 class="text-center">
                    {{card.front}}
                    <span id="answer"></span>
                </h1>
            </div>
            <ul class="list-group">
                <li v-for="option,index in card_options" :key="index" class="list-group-item">
                    <input class="form-check-input" type="radio" name="_{{card.id}}" value="{{-option-}}"
                        id="{{option}}_{{loop.index}}">
                    <label class="form-check-label" for="{{option}}_{{loop.index}}">
                        {{option}}
                    </label>
                </li>
            </ul>
            <button onclick="return submitAnswer()" class="btn btn-primary w-25 mx-auto mt-3 d-block">
                <span id="submit_text">
                    Show answer
                </span>
                <div class="spinner-border d-none spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </button>

            <form action="{{ url_for('review.review_form_post', deck_id=deck.id) }}" class="d-none" name="afterSubmit" method="POST">
                <input type="text" name="next" id="next" value="{{card.next}}" hidden>
                <input type="text" name="response_id" id="response_id" hidden>
                <div class="sort_options">
                    <h5 class="d-block w-100 text-center">
                        Difficulty Level
                    </h5>
                    <div class="sorts mx-auto w-100">
                        <div class="option">
                            <input type="radio" name="difficulty" id="easy" value="1" hidden />
                            <label for="easy" class="shadow">
                                <span>Easy</span>
                            </label>
                        </div>
                        <div class="option">
                            <input type="radio" name="difficulty" id="modarate" value="2" checked hidden />
                            <label for="modarate" class="shadow">
                                <span>Moderate</span>
                            </label>
                        </div>
                        <div class="option">
                            <input type="radio" name="difficulty" id="hard" value="3" hidden />
                            <label for="hard" class="shadow">
                                <span>Hard</span>
                            </label>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            Next 
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: "DeckTest",
    data() {
        return {
            isFinish:false,
            card:{},
            final_cards:[],
            deck:[]
        };
    },
    computed: {
        card_options(){
            return this.card.options && this.card.options.filter(a => a !== undefined || a !== null)
        }
    },
    methods: {
        submitAnswer(e) {

            let forms = e.target;
            
            if(forms){
                forms.classList.add('was-validated')
                if (!forms.checkValidity()) {
                    return false;
                }
            }
            // var input = $(':radio[name=_{{card.id}}]').filter(':checked').val();

            // if(!input){
            //     return false
            // }

            // clearInterval(interval)
            
            // document.querySelector('#submit_text').classList.add('d-none')
            // document.querySelector('.spinner-border ').classList.remove('d-none')
            // var question_card = document.querySelector('.question_card')

            // $.ajax({
            //     method: "GET",
            //     url: '{{ url_for("review.check_answer") }}?card_id={{card.id}}&&time='+ prev + '&&answer='+input,
            //     dataType: 'json',
            //     async: false,
            //     success: function(data){
            //         console.log("success");
            //         if(data.redirect){
            //             return window.location.href = "/start_test/{{deck.id}}"
            //         }
            //         if(data.correct){
            //             question_card.classList.add('bg-success')
            //         }else{
            //             question_card.classList.add('bg-danger')
            //         }
                
            //         question_card.classList.add('show-answer')
                    
            //         document.querySelector('#answer').innerHTML = data.answer
            //         $(':radio[name=_{{card.id}}]').prop('disabled', true)
            //         document.querySelector('#submit_text').parentElement.remove()
            //         document.querySelector('form[name="afterSubmit"]').classList.remove('d-none')

            //         forms.querySelector('[name="response_id"]').value = data.response_id
            //     },
            //     failure: function(data){
            //         console.log("failure");
                    
            //         document.querySelector('#submit_text').classList.remove('d-none')
            //         document.querySelector('.spinner-border ').classList.add('d-none')
            //     },
                
            // });
        }
    },
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
}
.question_card h1{
    font-family: var(--font-medium);
    font-size: 1.7rem;
    transform-style: preserve-3d;
    perspective: 500px;
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
.Easy::before{
    background: seagreen;
}
.Moderate::before{
    background: yellowgreen;
}
.Hard::before{
    background: tomato;
}
</style>