<template>
    <div id="deck">
        <div class="container deckDetails">
            <div v-if="current_deck">
                <h1 class="headline">
                    {{ current_deck.name }}
                    <div class="float-end">
                        <div v-if="current_deck.created_by_id == user.id">
                            <a href="#!" @click.prevent="deleteDeck"
                                class="btn me-3 updateProfile btn-secondary d-inline-block">
                                Delete Deck
                            </a>
                            <router-link :to="{name:'AddCard', query:{deck:current_deck.id} }"
                                class="btn me-3 updateProfile d-inline-block">
                                Add Card
                            </router-link>
                            <button data-bs-toggle="modal" data-bs-target="#create_a_deck"
                                class="btn updateProfile me-3 d-inline-block">
                                Update Deck
                            </button>
                        </div>
                        <button @click.prevent="download_excel"  
                            v-if="current_deck.created_by_id != user.id && current_deck.cards && current_deck.cards.length > 0"
                            class="btn ms-auto me-0 updateProfile h-50" 
                            :disabled="isDownloadingExcel">
                            <span v-if="isDownloadingExcel">
                                {{isDownloadingExcel}}
                            </span>
                            <span v-else>
                                Download Excel
                            </span>
                        </button>
                    </div>
                </h1>
                <div class="deckRow">
                    <div
                        class="container bg-white mb-3 d-flex align-items-center deck justify-content-between"
                    >
                        <div>
                            <h1>
                                {{ current_deck.name }}
                            </h1>
                            <p>
                                For
                                {{
                                    current_deck.created_for ? current_deck.created_for : "All"
                                }}
                            </p>
                        </div>
                        <div class="right-text">
                            <p>
                                {{ current_deck.number_of_cards }}
                            </p>
                            <h6>~By {{ current_deck.user && current_deck.user.username }}</h6>
                            <p class="small text-secondary">
                                At {{ new Date(current_deck.created_at).toLocaleString('en-In') }}
                            </p>
                        </div>
                    </div>
                </div>

                <router-link v-if="current_deck.cards && current_deck.cards.length > 0"
                    :to="{ name:'DeckTest', params:{deck_id:current_deck.id}}"
                    class="btn updateProfile mb-5 mt-5 mx-auto d-block w-25 p-2 fs-4">
                    Start Test
                </router-link>
                <h6 v-else>No Questions Added</h6>
                <div v-if="current_deck.created_by_id == user.id" class="container">
                    <div class="mb-5 d-flex align-items-end form_div">
                        <form
                            class="w-50 ms-0"
                            @submit.prevent="uploadExcel($event)"
                        >
                            <h6>Upload Excel</h6>
                            <div class="input-group">
                                <input
                                    type="file"
                                    class="form-control"
                                    id="file"
                                    aria-describedby="file"
                                    aria-label="Upload"
                                    required
                                    name="importFile"
                                    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, .xlsx, .xls"
                                />
                                <button
                                    class="btn btn-secondary"
                                    type="submit"
                                    id="file"
                                >
                                    Upload
                                </button>
                            </div>
                        </form>
                        <button @click.prevent="download_excel"
                            class="btn ms-auto me-0 updateProfile h-50"
                            v-if="current_deck.cards && current_deck.cards.length > 0"
                            :disabled="isDownloadingExcel">
                            <span v-if="isDownloadingExcel">
                                {{isDownloadingExcel}}
                            </span>
                            <span v-else>
                                Download Excel
                            </span>
                        </button>
                    </div>
                    <create-deck :isUpdate="true" :deck="current_deck" />
                    <div class="row">
                        <div v-for="(card, index) in current_deck.cards || []" :key="index"
                            class="mb-3 card col-lg-4 col-md-4 col-sm-6 col-xs-12">
                            <div class="card-body" style="min-height: 8em">
                                <h1 class="fs-5">{{ card.front }}</h1>
                            </div>
                            <div class="card-footer bg-transparent">
                                <router-link :to="{ name:'EditCard', params:{card_id:card.id} }"
                                    class="btn mb-2 updateProfile d-block">
                                    Edit Card
                                </router-link>
                                <a href="#!" class="btn updateProfile btn-secondary d-block"
                                    @click.prevent="deleteCard(card.id)"
                                >
                                    Delete Card
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else-if="!current_deck && !loader" class="deckRow text-center">
                <h1 class="">No Deck Found!</h1>
                <p class="text-secondary">Please check id</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapActions, mapGetters } from 'vuex';
import { REMOTE_URL, fromBase64ToFile } from "@/constants/constant";
import CreateDeck from "../Home/CreateDeck.vue";
export default {
    components: { CreateDeck },
    name: "ViewDeck",
    data() {
        return {
            source:null,
            isDownloadingExcel:null,
        };
    },
    computed: {
        ...mapGetters(["current_deck", "user", "loader"])
    },
    methods: {
        ...mapActions(["set_loader", "set_current_deck", "set_error_message", "set_toast_message"]),
        download_excel(){
            this.set_loader(true)
            axios.get(REMOTE_URL + "download_deck/" + this.current_deck.id, {
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }).then(res=>{
                this.set_loader(false);
                if(res.data.success){
                    this.set_toast_message(res.data.message)
                }
            }).catch(err=>{
                this.set_error_message(err);
                this.set_loader(false)
            })
        },
        uploadExcel(e){
            this.set_loader(true)
            let formData = new FormData(e.target);
            formData.append("deck_id", this.current_deck.id)
            axios.post(REMOTE_URL + "upload", formData, {
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }).then(res=>{
                if(res.data.success){
                    this.set_current_deck(this.$route.params.deck_id).then(()=>{
                        this.set_loader(false);
                    })
                }else{
                    this.set_loader(false);
                }
                this.set_toast_message(res.data.message)
            }).catch(err=>{
                this.set_error_message(err);
                this.set_loader(false)
            })
        },
        delete(endpoint){
            this.set_loader(true)
            return axios.delete(REMOTE_URL + endpoint, {
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }).catch(err=>{
                this.set_error_message(err);
                this.set_loader(false)
            })
        },
        deleteDeck(){
            if(this.current_deck && confirm("Are you sure do you want to delete it?")){
                this.delete("deck/" + this.current_deck.id).then(res=>{
                    if(res.data.status){
                        this.set_error_message("Successfully deleted deck")
                        this.$router.push("/")
                    }
                    this.set_loader(false)
                })
            }
        },
        deleteCard(card_id){
            if(card_id && confirm("Are you sure do you want to delete it?")){
                this.delete("card/" + card_id).then(res=>{
                    if(res.data.status){
                        this.set_error_message("Successfully deleted card")
                        this.current_deck.cards = this.current_deck.cards.filter(a=> a.id !== card_id)
                    }
                    this.set_loader(false)
                })
            }
        }
    },
    created(){
        this.set_loader(true);
        this.set_current_deck(this.$route.params.deck_id).then(()=>{
            this.set_loader(false);
        })
    },
    
    mounted(){
        var vm = this;
        this.source = new EventSource(REMOTE_URL.replace('api/', '') + "stream?channel=" + this.user.email + "_" + this.user.id);
        this.source.addEventListener('excel', function(event) {
            var data = JSON.parse(event.data);
            vm.isDownloadingExcel = data.message;
            if(data.file){
                const downloadLink = document.createElement("a");
                let fileName = data.filename;
                let file = fromBase64ToFile(data.file)
                downloadLink.href = file;
                downloadLink.download = fileName;
                downloadLink.click();
                vm.set_toast_message("Your file is downloaded")
            }
            if(data.isDone){
                vm.isDownloadingExcel = null;
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
#deck {
    position: relative;
    height: 100%;
}
#deck .container {
    padding: 10px 15px;
    background: var(--backgroundColor);
}
#deck .deckDetails {
    max-width: 70%;
    margin-bottom: 100px;
}
.right-text {
    text-align: right;
}
.deck h1 {
    font-size: 1.3rem;
    font-family: var(--font-medium);
    margin-bottom: 5px;
}
.deck h6 {
    font-size: 0.95rem;
    font-family: var(--font-medium);
    margin-bottom: 0;
}
.btn.updateProfile {
    border: var(--buttonColor) 1px solid;
    background: var(--buttonColor);
    border-radius: 50px;
    color: white;
    font-size: 1.1rem;
    height: auto;
    padding: 2px 25px;
    font-family: Poppins Regular, sans-serif;
    cursor: pointer;
    text-transform: capitalize;
}
.btn.updateProfile.btn-secondary {
    color: #fff;
    background-color: #6c757d;
    border-color: #6c757d;
}
@media screen and (max-width:992px){
    #deck .deckDetails{
        max-width: 90%;
        margin-bottom: 100px;
    }
}

@media screen and (max-width:600px){
    .headline .float-end{
        float:none !important;
    }
    .btn.updateProfile {
        width: 100% !important;
    }
}

@media screen and (max-width:500px){
    .deckRow .deck{
        flex-wrap: wrap;
    }
    .deckRow .deck div{
        width:100%;
        text-align:center !important;
    }
    
    .container .form_div{
        flex-wrap: wrap;
        row-gap: 15px;
    }
    .container form{
        width: 100% !important;
    }
}
</style>