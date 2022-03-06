<template>
    <div id="add_card">
    <div class="container add_cardDetails">
        <h1 v-if="userDecks.length === 0" class="fs-4 text-center">
            Please add a deck from 
            <router-link style="color: #0d6efd;" to="/">here</router-link> to continue
        </h1>
        <form v-else class="needs-validation" novalidate @submit.prevent="submitForm">
            <div class="modal-body">
                <div class="mb-3">
                    <label for="deck" class="form-label">Deck</label>
                    <select class="form-select" id="deck" name="deck_id" aria-label="Deck" required>
                        <option v-for="deck in userDecks" :key="deck.id"
                            :value="deck.id" :selected="card && card.deck_id==deck.id || deck_id==deck.id">
                            {{deck.name}}
                        </option>
                        
                    </select>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="front" class="form-label">Front</label>
                    <input type="text" class="form-control" id="front" name="front" 
                        :v-model="card.front" placeholder="Enter front" required>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="back" class="form-label">Back</label>
                    <input type="text" class="form-control" id="back" name="back" 
                        v-model="card.back" placeholder="Enter Back" required>
                    <div class="invalid-feedback">
                        Please enter valid input
                    </div>
                </div>
                <div class="mb-3">
                    <label for="options" class="form-label">Options</label>
                    <textarea class="form-control" id="options" name="options" rows="3"  
                        required v-model="card.options">
                    </textarea>
                    <div class="helpText">
                        Separate by comma ","
                    </div>
                    <div class="invalid-feedback">
                        Please enter options
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <a href="{{url_for('deck.view_deck', deck_id=card.deck_id) if card else url_for('profile.home') }}" class="btn btn-secondary">Close</a>
                <button type="submit" class="btn btn-primary">Save changes</button>
            </div>
        </form>
    </div>
</div>
</template>

<script>
export default {
    name:"AddCardForm",
    data(){
        return{
            userDecks:[{
                id:5,
                name:"Tree"
            }],
            card:{},
            deck_id:null,
        }
    },
    methods:{
        submitForm(e){
            //  action="{{url_for('card.edit_card', card_id=card.id) 
            //  if card else url_for('card.add_card') }}"
            //   method="POST"
            let forms = e.target;
            forms.classList.add('was-validated')
            if (!forms.checkValidity()) {
                return false;
            }
        }
    }
}
</script>

<style scoped>
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


</style>