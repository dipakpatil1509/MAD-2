<template>
    <div v-if="current_response" class="result">
        <h1 class="text-center fs-4 mt-5">Congratulations! You have completed the deck!</h1>
        <div class="progress mt-5 w-50 mx-auto bg-danger" style="height:25px;">
            <div class="progress-bar bg-success" :style="'width:'+current_response.score + '%'" id="progressBar" role="progressbar">
                {{current_response.score}}%
            </div>
        </div>
        <div class="mx-auto d-block w-75 result-div">
            <div class="avg_time mt-4">
                <h3 class="fs-5">Averge time :- {{ get_time(current_response.avg_time) }} sec</h3>
            </div>
            <div class="completed_at">
                <h3 class="fs-5">Completed At :- {{ current_response.completed_at }}</h3>
            </div>
            <div class="download">
                <button @click.prevent="download_report(true)"
                    class="btn updateProfile h-50" :disabled="isDownloadingPDF">
                    <span v-if="isDownloadingPDF">
                        {{isDownloadingPDF}}
                    </span>
                    <span v-else>
                        Download Report as pdf
                    </span>
                </button>
                <button @click.prevent="download_report(false)"
                    class="btn updateProfile h-50" :disabled="isDownloadingHTML">
                    <span v-if="isDownloadingHTML">
                        {{isDownloadingHTML}}
                    </span>
                    <span v-else>
                        Download Report as HTML
                    </span>
                </button>
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
                            <td>{{ get_time(item.time) }} secs</td>
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
import { REMOTE_URL, fromBase64ToFile } from "@/constants/constant";
import axios from 'axios';
export default {
    name: "DeckTestResult",
    data() {
        return {
            source:undefined,
            isDownloadingPDF:null,
            isDownloadingHTML:null
        };
    },
    computed: {
        ...mapGetters(["current_response", "user"])
    },
    methods: {
        ...mapActions([
            "set_current_response", "set_loader", "set_toast_message"
        ]),
        get_time(time){
            if(time > 0){
                var minutes = Math.floor(time / 60000);
                var seconds = ((time % 60000) / 1000).toFixed(0);
                return (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00"
        },
        download_report(pdf){
            let endpoint = "report/" + this.$route.params.response_id
            if(pdf){
                endpoint += "?pdf=true"
            }
            axios.get(REMOTE_URL + endpoint, {
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }).then(res=>{
                if(res.data.success){
                    this.set_toast_message(res.data.message);
                }
            })
        }
    },
    watch:{
    },
    created(){
        this.set_loader(true);
        this.set_current_response(this.$route.params.response_id).then(()=>{
            this.set_loader(false);
        })
    },
    mounted(){
        var vm = this;
        console.log(REMOTE_URL.replace('api/', '') + "stream");
        this.source = new EventSource(REMOTE_URL.replace('api/', '') + "stream?channel=" + this.user.email + "_" + this.user.id);
        this.source.addEventListener('report', function(event) {
            var data = JSON.parse(event.data);
            console.log(data);
            if(data.pdf){
                vm.isDownloadingPDF = data.message;
            }else{
                vm.isDownloadingHTML = data.message;
            }
            if(data.file){
                const downloadLink = document.createElement("a");
                let extension = ".html";
                let file =  data.file;
                let fileName = vm.current_response.deck.name + extension;
                if(data.pdf){
                    file = fromBase64ToFile(data.file)
                    fileName = vm.current_response.deck.name + '.pdf';
                }else{
                    file="data:text/html;charset=UTF-8," + encodeURIComponent(file)
                }

                downloadLink.href = file;
                downloadLink.download = fileName;
                downloadLink.click();
                vm.set_toast_message("Your file is downloaded")
                if(data.pdf){
                    vm.isDownloadingPDF = null;
                }else{
                    vm.isDownloadingHTML = null;
                }
            }
        }, false);
        this.source.addEventListener('error', (event)=>{
            console.log(event);
            this.set_toast_message("Failed to connect to the server");
        }, false);

    },

    unmounted(){
        if(this.source){
            this.source.close()
        }
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
.download{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap:10px;
    justify-content: flex-end;
    margin: 20px 0;
}
.btn.updateProfile {
    border: var(--buttonColor) 1px solid;
    background: var(--buttonColor);
    border-radius: 50px;
    color: white;
    font-size: 1.1rem;
    height: auto;
    padding: 2px 25px;
    margin:0;
    font-family: Poppins Regular, sans-serif;
    cursor: pointer;
    text-transform: capitalize;
    min-width: 300px;
}

.btn.updateProfile:disabled{
    background: rgba(var(--buttonColorRGB), 0.7);
}

.question_type{
    overflow-x: auto;
}
@media screen and (max-width:800px){
    .result{
        padding: 0 10px ;
    }
    .result-div {
        width: 100% !important;
    }
}

@media screen and (max-width:650px){
    .btn.updateProfile {
        min-width: 100%;
    }
    .progress{
        width:100% !important;
    }
}

</style>