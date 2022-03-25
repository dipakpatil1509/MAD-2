<template>
     <div class="modal fade" id="create_a_deck" aria-labelledby="create_a_deckLabel" aria-hidden="true" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{isUpdate ? 'Update ' + deck.name : 'Create A Deck'}}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form name="createForm" class="needs-validation" 
                        novalidate @submit.prevent="submitForm">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" name="name" 
                                    placeholder="Enter Name" required v-model="currentDeck.name">
                                <div class="invalid-feedback">
                                    Please enter valid name
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Tag</label>
                                <div class="d-flex justify-content-start">
                                    <div>
                                        <input class="form-check-input" type="radio" 
                                        name="created_for" value="STUDENT" id="student" v-model="currentDeck.created_for">
                                        <label class="form-check-label" for="student">
                                            Student
                                        </label>
                                    </div>
                                    <div  class="ms-4">
                                        <input class="form-check-input" type="radio" name="created_for" 
                                        value="TEACHER" id="teacher" v-model="currentDeck.created_for">
                                        <label class="form-check-label" for="teacher">
                                            Teacher
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="created_for" class="form-label">Do you want deck to be public?</label>
                                <select class="form-select" id="created_for" name="public_status" 
                                aria-label="Default select example" required v-model="currentDeck.public_status">
                                    <option value="1" selected>Yes</option>
                                    <option value="0">No</option>
                                </select>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Save changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<script>
import { mapActions } from 'vuex';
import { Modal } from 'bootstrap';
import axios from 'axios';
import { REMOTE_URL } from "@/constants/constant"
export default {
    name:"CreateADeck",
    props:['isUpdate', 'deck'],
    data(){
        return{
            currentDeck:{
                name:"",
                created_for:"",
                public_status:"1",
            },
        }
    },
    methods:{
        ...mapActions(["set_loader", "set_toast_message", "set_error_message", "set_current_deck"]),
        submitForm(e){
            var forms = e.target;
            forms.classList.add('was-validated')
            if (!forms.checkValidity()) {
                return
            }

            this.set_loader(true)
            console.log(this.currentDeck);
            
            let config = {
                method:"POST",
                url:REMOTE_URL + "deck", 
                data:this.currentDeck,
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }
            if(this.isUpdate){
                config.method = "PUT"
                config.url += "/" + this.deck.id
            }
            axios(config).then(res=>{
                if(res.data.error_code){
                    throw Error(res.data.error_message)
                }
                this.$emit('get_decks')
                this.currentDeck = !this.isUpdate ? {
                    name:"",
                    created_for:"",
                    public_status:"1",
                } : this.deck
                forms.classList.remove('was-validated')
                var modal = Modal.getInstance(document.querySelector('#create_a_deck'))
                modal.hide();
                if(this.isUpdate){
                    this.set_current_deck(this.currentDeck.id)
                }
                this.set_loader(false);
                this.set_toast_message("Successfully added deck")
            }).catch(err=>{
                this.set_loader(false)
                this.set_error_message(err)
            })
        }
    },
    watch:{
        deck:{
            handler(val){
                if(val){
                    val.public_status = val.public_status ? '1' : '0'
                    this.currentDeck = {...val}
                }
            },
            immediate: true, 
        }
    },
    beforeUnmount(){
        let elm = document.querySelector('#create_a_deck')
        if(elm){
            var modal = Modal.getInstance(elm)
            if(modal){
                modal.hide();
            }
        }
    }
}
</script>

<style scoped>
form{
    margin:0;
    padding: 0 !important;
}
label{
    text-transform: none;
}
label:not(.form-check-label){
    font-family: var(--font-medium);
}
label.form-check-label{
    font-family: var(--font-regular);
    margin-left: 5px;
}
</style>