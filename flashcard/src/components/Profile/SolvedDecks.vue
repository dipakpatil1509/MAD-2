<template>
    <h1 class="headline">All Reviewed</h1>
    <div class="download">
        <button @click.prevent="download_report(true, true)"
            class="btn updateProfile h-50" :disabled="isMonthlyDownloadingPDF">
            <span v-if="isMonthlyDownloadingPDF">
                {{isMonthlyDownloadingPDF}}
            </span>
            <span v-else>
                Download Monthly Report as pdf
            </span>
        </button>
        <button @click.prevent="download_report(true, false)"
            class="btn updateProfile h-50" :disabled="isAllTimeDownloadingPDF">
            <span v-if="isAllTimeDownloadingPDF">
                {{isAllTimeDownloadingPDF}}
            </span>
            <span v-else>
                Download All Time as PDF
            </span>
        </button>
        <button @click.prevent="download_report(false, true)"
            class="btn updateProfile h-50" :disabled="isMonthlyDownloadingHTML">
            <span v-if="isMonthlyDownloadingHTML">
                {{isMonthlyDownloadingHTML}}
            </span>
            <span v-else>
                Download Monthly Report as HTML
            </span>
        </button>
        <button @click.prevent="download_report(false, false)"
            class="btn updateProfile h-50" :disabled="isAllTimeDownloadingHTML">
            <span v-if="isAllTimeDownloadingHTML">
                {{isAllTimeDownloadingHTML}}
            </span>
            <span v-else>
                Download All Time Report as HTML
            </span>
        </button>
    </div>
    <div class="question_type">
        <table class="table text-center">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Tag</th>
                    <th scope="col">Score</th>
                    <th scope="col">Avg Time</th>
                    <th scope="col">Completed at</th>
                </tr>
            </thead>
            <tbody class="fs-6">
                <tr v-for="(item, index) in decks" :key="index">
                    <th scope="row">1</th>
                    <td>
                        <router-link
                            :to="{
                                name: 'Result',
                                params: { response_id: item.id },
                            }"
                            class="fs-6 mt-0"
                        >
                            {{ item.deck.name }}
                        </router-link>
                    </td>
                    <td>{{ item.deck.created_for }}</td>
                    <td>{{ item.score }}</td>
                    <td>{{ get_time(item.avg_time) }} secs</td>
                    <td>{{ item.completed_at }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { REMOTE_URL, fromBase64ToFile } from "@/constants/constant";
import axios from 'axios';
export default {
    name:"SolvedDecks",
    props:["decks"],
    data(){
        return{
            source:null,
            isMonthlyDownloadingPDF:null,
            isMonthlyDownloadingHTML:null,
            isAllTimeDownloadingPDF:null,
            isAllTimeDownloadingHTML:null,
        }
    },
    computed: {
        ...mapGetters(["user"])
    },
    methods: {
        ...mapActions([
            "set_toast_message"
        ]),
        get_time(time){
            if(time > 0){
                var minutes = Math.floor(time / 60000);
                var seconds = ((time % 60000) / 1000).toFixed(0);
                return (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00"
        },
        download_report(pdf, monthly){
            let endpoint = "report/0?"
            if(pdf){
                endpoint += "pdf=true&"
            }
            if(!monthly){
                endpoint += "isAll=true"
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
    
    mounted(){
        var vm = this;
        console.log(REMOTE_URL.replace('api/', '') + "stream");
        this.source = new EventSource(REMOTE_URL.replace('api/', '') + "stream?channel=" + this.user.email + "_" + this.user.id);
        this.source.addEventListener('report', function(event) {
            var data = JSON.parse(event.data);
            console.log(data);
            if(data.pdf){
                if(data.monthly){
                    vm.isMonthlyDownloadingPDF = data.message
                }
                if(data.allTime){
                    vm.isAllTimeDownloadingPDF = data.message
                }
            }else{
                if(data.monthly){
                    vm.isMonthlyDownloadingHTML = data.message
                }
                if(data.allTime){
                    vm.isAllTimeDownloadingHTML = data.message
                }
            }
            if(data.file){
                const downloadLink = document.createElement("a");
                let extension = ".html";
                let name = "all_time_report";
                if(data.monthly){
                    name = "monthly_report"
                }
                let file =  data.file;
                let fileName = name + extension;
                if(data.pdf){
                    file = fromBase64ToFile(data.file)
                    fileName = name + '.pdf';
                }else{
                    file="data:text/html;charset=UTF-8," + encodeURIComponent(file)
                }

                downloadLink.href = file;
                downloadLink.download = fileName;
                downloadLink.click();

                vm.set_toast_message("Your file is downloaded")
                
                if(data.pdf){
                    if(data.monthly){
                        vm.isMonthlyDownloadingPDF = null
                    }
                    if(data.allTime){
                        vm.isMonthlyDownloadingHTML = null
                    }
                }else{
                    if(data.monthly){
                        vm.isMonthlyDownloadingHTML = null
                    }
                    if(data.allTime){
                        vm.isAllTimeDownloadingHTML = null
                    }
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
a{
    color: #000;
    font-size: 1.1rem;
    font-weight: 600;
}

.download{
    display: flex;
    flex-wrap: wrap;
    /* align-items: center; */
    gap:10px;
    justify-content: space-evenly;
    margin: 20px 0;
}
.btn.updateProfile {
    border: var(--buttonColor) 1px solid;
    background: var(--buttonColor);
    border-radius: 50px;
    color: white;
    font-size: 1.1rem;
    height: unset !important;
    padding: 10px 25px;
    margin:0;
    font-family: Poppins Regular, sans-serif;
    cursor: pointer;
    text-transform: capitalize;
    min-width: 250px;
    max-width: calc(25% - 20px);
    line-height: 1.3rem;
}

.btn.updateProfile:disabled{
    background: rgba(var(--buttonColorRGB), 0.7);
}
.question_type{
    overflow-x: auto;
}
</style>