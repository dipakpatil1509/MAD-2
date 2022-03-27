<template>
    <div id="add_card">
    <div class="container add_cardDetails">
        <h1 v-if="decks.length === 0 && !loader" class="fs-4 text-center">
            Please add a deck from 
            <router-link style="color: #0d6efd;" to="/">here</router-link> to continue
        </h1>
        <form v-else-if="decks.length > 0" class="needs-validation" novalidate @submit.prevent="submitForm">
            <div class="modal-body">
                <div class="mb-3">
                    <label for="deck" class="form-label">Deck</label>
                    <select class="form-select" id="deck" name="deck_id" aria-label="Deck" 
                        v-model="card.deck_id" required>
                        <option v-for="deck in decks" :key="deck.id" :value="deck.id">
                            {{deck.name}}
                        </option>
                        
                    </select>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="front" class="form-label">Front</label>
                    <input type="text" class="form-control" id="front" autocomplete="off" name="front" 
                        v-model="card.front" placeholder="Enter front" required>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="back" class="form-label">Back</label>
                    <input type="text" class="form-control" id="back"  autocomplete="off" name="back" 
                        v-model="card.back" placeholder="Enter Back" required>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="options" class="form-label">Options</label>
                    <textarea class="form-control" id="options" name="options" rows="5"  
                        required v-model="card.options" :readonly="!card.back"
                        :placeholder="card.back ? 'Write options with comma separated' :'Please add card answer first'">
                    </textarea>
                    <div class="helpText">
                        Separate by comma ","
                        <br>
                        Dont't need to write answer again
                        <br>
                        <span v-if="card.back">
                            Final Options :- 
                            {{card.back}}, {{ card.options }}
                        </span>
                    </div>
                    <div class="invalid-feedback">
                        Please enter options
                    </div>
                </div>
                <div class="input-group">
                    <label for="optionsCSV" class="form-label">Add options with CSV</label>
                    <input type="file" class="form-control" id="optionsCSV" name="optionsCSV"
                       :disabled="!card.back" aria-describedby="file" aria-label="Upload" accept=".csv" @input="addoptionswithcsv"
                    />
                </div>
            </div>
            <div class="modal-footer">
                <a href="#!" @click.prevent="$router.go(-1)" class="btn btn-secondary">
                    Go back
                </a>
                <button type="submit" class="btn btn-primary">
                    Save changes
                </button>
            </div>
        </form>
    </div>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios';
import { REMOTE_URL } from "@/constants/constant";

export default {
    name:"AddCardForm",
    data(){
        return{
            card:{
                deck_id:'',
                front:"",
                back:"",
                options:""
            },
            isUpdate:false
        }
    },
    computed:{
        ...mapGetters(["decks", "loader", 'current_card']),
    },
    methods:{
        ...mapActions([
            "set_decks", "set_loader", "set_loader_message", 
            "set_toast_message", "set_error_message", "set_current_card"
        ]),
        addoptionswithcsv(e){
            if(e.target.files.length > 0){
                var reader = new FileReader();
                reader.onload = ()=>{
                    this.card.options = reader.result;
                };
                reader.readAsBinaryString(e.target.files[0]);
            }
        },
        submitForm(e){
            let forms = e.target;
            forms.classList.add('was-validated')
            if (!forms.checkValidity()) {
                return false;
            }

            Object.keys(this.card).forEach(elem=>{
                if(!this.card[elem]){
                    this.set_loader_message("Please fill information for " + elem)
                    return 
                }
            })

            let data = {...this.card};
            data.options += ', ' + data.back

            console.log(data);
            this.set_loader(true)
            
            let config = {
                method:"POST",
                url:REMOTE_URL + "card", 
                data:data,
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                    "Content-type":"application/json"
                }
            }
            if(this.isUpdate){
                config.method = "PUT"
                config.url += "/" + this.current_card.id
            }
            axios(config).then(res=>{
                if(res.data.error_code){
                    throw Error(res.data.error_message)
                }
                forms.classList.remove('was-validated')
                if(!this.isUpdate) {
                    Object.assign(this.$data, this.$options.data()) 
                }else{
                    Object.assign(this.$data, this.current_card) 
                }
                this.set_loader(false);
                this.set_toast_message("Successfully added card")
            }).catch(err=>{
                this.set_loader(false)
                console.log(err);
                this.set_error_message(err)
            })
        }
    },
    watch:{
        "$route":{
            handler(val){
                this.card.deck_id = val.query.deck
            },
            immediate:true,
            deep:true
        }, 
        "current_card":{
            handler(val){
                if(val){
                    val.options = val.options.split(',').filter(res=> res.trim() !== val.back).join(',')
                    this.card = {...val}
                    this.isUpdate = true
                }
            },
            immediate:true,
        }
    },
    created(){
        this.set_loader(true)
        this.set_decks(2).then(()=>{
            if(!this.current_card)
                this.set_loader(false)
        })
        
        this.set_loader(true)
        this.set_current_card(this.$route.params.card_id).then(()=>{
            this.set_loader(false)
        })
    }
}
</script>

<style scoped>
textarea{
    resize: none;
}
input[type="file"]{
    display: block;
    width: 100%;
}
.modal-footer{
    justify-content: space-between;
}
#add_card{
    position: relative;
    height: 100%;
}
#add_card .container{
    padding:10px 15px;
    background: var(--backgroundColor);
}
#add_card .add_cardDetails{
    max-width:70%;
    margin-bottom: 100px;
}
#add_card .row{
    margin:0;
}
.right-text{
    text-align: right;
}
.add_card h1{
    font-size: 1.3rem;
    font-family: var(--font-medium);
    margin-bottom: 5px;
}
.add_card h6{
    font-size: 0.95rem;
    font-family: var(--font-medium);
    margin-bottom: 0;
}
.add_cardDetails .row, .add_cardDetails form{
    margin:0;
    padding: 0 !important;
}
.add_cardDetails form .input-field.col{
    padding-left: 0 !important;
}
.add_cardDetails form .input-field.col label{
    left:0;
}
.btn.updateProfile{
    border: var(--buttonColor) 1px solid;
    background:var(--buttonColor);
    border-radius: 50px;
    color:white;
    font-size:1.1rem;
    height: auto;
    padding: 2px 25px;
    font-family: Poppins Regular, sans-serif;
    cursor: pointer;
    text-transform: capitalize;
}
.btn.updateProfile.btn-secondary{
    color: #fff;
    background-color: #6c757d;
    border-color: #6c757d;
}


@media screen and (max-width:992px){
    #add_card .add_cardDetails{
        max-width: 90%;
        margin-bottom: 100px;
    }
}
</style>