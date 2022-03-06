<template>
     <div class="modal fade" id="create_a_deck" aria-labelledby="create_a_deckLabel" aria-hidden="true" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{isUpdate ? 'Update' : 'Create'}} A Deck</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form name="createForm" class="needs-validation" 
                        novalidate @submit.prevent="submitForm">
                        <div class="modal-body">
                            <div class="text-danger">
                                {{ errors }}
                            </div>
                            <div class="mb-3">
                                <input type="text" name="user_id" hidden value="{{user.id}}">

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
                                        name="created_for" value="STUDENT" id="student" v-model="currentDeck.role">
                                        <label class="form-check-label" for="student">
                                            Student
                                        </label>
                                    </div>
                                    <div  class="ms-4">
                                        <input class="form-check-input" type="radio" name="created_for" 
                                        value="TEACHER" id="teacher" v-model="currentDeck.role">
                                        <label class="form-check-label" for="teacher">
                                            Teacher
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="created_for" class="form-label">Public</label>
                                <select class="form-select" id="created_for" name="public_status" 
                                aria-label="Default select example" required v-model="currentDeck.status">
                                    <option value="1" selected>True</option>
                                    <option value="0">False</option>
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
export default {
    name:"CreateADeck",
    props:['isUpdate', 'deck'],
    data(){
        return{
            errors:"",
            currentDeck:this.deck || {},
        }
    },
    methods:{
        submitForm(e){
            var forms = e.target;
            forms.classList.add('was-validated')
            if (!forms.checkValidity()) {
                return
            }
            // action="{{ url_for('deck.add_deck') }}"
            // method="POST"
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