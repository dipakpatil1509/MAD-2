<template>
    <div
        class="modal fade"
        id="updateProfile"
        aria-labelledby="updateProfileLabel"
        aria-hidden="true"
        tabindex="-1"
    >
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Update Profile</h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <form
                    name="updateForm"
                    class="needs-validation"
                    novalidate
                    @submit.prevent="submitForm"
                >
                    <div class="modal-body">
                        <div class="text-danger">
                            {{ errors }}
                        </div>
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input
                                type="text"
                                class="form-control"
                                id="name"
                                name="name"
                                placeholder="Enter Name"
                                v-model="user.name"
                            />
                        </div>
                        <div class="mb-3 d-flex justify-content-evenly">
                            <div>
                                <input class="form-check-input" type="radio"
                                name="role" value="STUDENT" v-model="user.role"
                                id="student">
                                <label class="form-check-label" for="student">
                                    Student
                                </label>
                            </div>
                            <div>
                                <input class="form-check-input" type="radio"
                                name="role" value="TEACHER" v-model="user.role"
                                id="teacher">
                                <label class="form-check-label" for="teacher">
                                    Teacher
                                </label>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="exampleInputEmail1" class="form-label"
                                >Email address</label
                            >
                            <input
                                type="email"
                                class="form-control"
                                id="exampleInputEmail1"
                                aria-describedby="emailHelp"
                                name="email"
                                readonly
                                disabled
                                placeholder="abcd@abcd.com"
                                v-model="user.email"
                                required
                            />
                        </div>
                        <div class="mb-3">
                            <label for="currentPassword" class="form-label"
                                >Current Password</label
                            >
                            <input
                                type="password"
                                name="currentPassword"
                                class="form-control"
                                id="currentPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                            />
                            <div class="invalid-feedback">
                                Please enter valid password Must be 8-20
                                characters long.
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="newPassword" class="form-label"
                                >New Password</label
                            >
                            <input
                                type="password"
                                name="newPassword"
                                class="form-control"
                                id="newPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                            />
                            <div class="invalid-feedback">
                                Please enter valid password Must be 8-20
                                characters long.
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="confirmNewPassword" class="form-label"
                                >Confirm New Password</label
                            >
                            <input
                                type="password"
                                name="confirmNewPassword"
                                class="form-control"
                                id="confirmNewPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                            />
                            <div class="invalid-feedback">
                                Please enter valid password Must be 8-20
                                characters long.
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button type="submit" class="btn btn-primary">
                            Save changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name:"UpdateDetailsModal",
    data(){
        return{
            errors:"",
            user:{}
        }
    },
    methods:{
        submitForm(e){
            var empty = "Must Not Be Empty";
            var notMatch = "Password Not Matching"
            let forms = e.target;
            forms.classList.add('was-validated')
            if (!forms.checkValidity()) {
                return
            }

            let currentPassword = forms['currentPassword'].value

            if (currentPassword) {
                let newPassword = forms['newPassword'].value
                let confirmNewPassword = forms['confirmNewPassword'].value
                if (!(newPassword !== '' && confirmNewPassword !== '' && newPassword === confirmNewPassword)) {
                    event.preventDefault()
                    event.stopPropagation()
                    if (newPassword === "" || confirmNewPassword === "") {

                        if (newPassword === "") {
                            forms['newPassword'].classList.add('is-invalid')
                            forms['newPassword'].setCustomValidity('Empty Not Valid')
                            forms['newPassword'].parentElement.querySelector('.invalid-feedback').innerHTML = empty
                        }
                        if (confirmNewPassword === "") {
                            forms['confirmNewPassword'].parentElement.querySelector('.invalid-feedback').innerHTML = empty
                            forms['confirmNewPassword'].classList.add('is-invalid')
                            forms['confirmNewPassword'].setCustomValidity('Empty Not Valid')
                        }

                    }
                    else if (newPassword !== confirmNewPassword) {
                        forms['confirmNewPassword'].classList.add('is-invalid')
                        forms['confirmNewPassword'].setCustomValidity('Password not match')
                        forms['confirmNewPassword'].parentElement.querySelector('.invalid-feedback').innerHTML = notMatch
                    }
                } else {
                    forms['newPassword'].classList.add('is-valid')
                    forms['newPassword'].setCustomValidity('')
                    forms['confirmNewPassword'].classList.add('is-valid')
                    forms['confirmNewPassword'].setCustomValidity('')
                }
            }
            // action="{{ url_for('profile.profileUpdate') }}"
            // method="POST"
        }
    },
    mounted(){

    }
};
</script>

<style scoped>
form{
    margin:0;
    padding: 0 !important;
}
form .input-field.col{
    padding-left: 0 !important;
}
form .input-field.col label{
    left:0;
}
</style>