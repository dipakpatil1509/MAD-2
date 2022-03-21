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
                    <div class="modal-body row">
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="name" class="form-label">Name</label>
                            <input
                                type="text"
                                class="form-control"
                                id="name"
                                name="name"
                                required
                                placeholder="Enter Name"
                                v-model="currentUser.username"
                            />
                        </div>
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="email" class="form-label">
                                Email address
                            </label>
                            <input
                                type="email"
                                class="form-control"
                                id="email"
                                aria-describedby="emailHelp"
                                name="email"
                                readonly
                                disabled
                                placeholder="abcd@abcd.com"
                                v-model="currentUser.email"
                                required
                            />
                        </div>
                        <div class="mb-3 d-flex col-md-6 col-sm-12 flex-wrap align-items-center">
                            <div class="w-100">
                                <label class="form-label">
                                    Are you a student or a teacher?
                                </label>
                            </div>
                            <div>
                                <input
                                    class="form-check-input"
                                    type="radio"
                                    name="role"
                                    value="STUDENT"
                                    v-model="currentUser.role"
                                    id="student"
                                />
                                <label class="form-check-label" for="student">
                                    Student
                                </label>
                            </div>
                            <div class="mx-2">
                                <input
                                    class="form-check-input"
                                    type="radio"
                                    name="role"
                                    value="TEACHER"
                                    v-model="currentUser.role"
                                    id="teacher"
                                />
                                <label class="form-check-label" for="teacher">
                                    Teacher
                                </label>
                            </div>
                        </div>
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="phone" class="form-label">
                                Mobile Number
                            </label>
                            <input
                                type="tel"
                                class="form-control"
                                id="phone"
                                aria-describedby="emailHelp"
                                name="phone"
                                placeholder="+910000000000"
                                v-model="currentUser.mobile_number"
                            />
                        </div>
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="currentPassword" class="form-label">
                                Current Password
                            </label>
                            <input
                                type="password"
                                name="currentPassword"
                                class="form-control"
                                id="currentPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                                v-model="oldPassword"
                            />
                            <div class="invalid-feedback">
                                Please enter valid password Must be 8-20
                                characters long.
                            </div>
                        </div>
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="newPassword" class="form-label">
                                New Password
                            </label>
                            <input
                                type="password"
                                name="newPassword"
                                class="form-control"
                                id="newPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                                v-model="newPassword"
                            />
                            <div class="invalid-feedback">
                                Please enter valid password Must be 8-20
                                characters long.
                            </div>
                        </div>
                        <div class="mb-3 col-md-6 col-sm-12">
                            <label for="confirmNewPassword" class="form-label">
                                Confirm New Password
                            </label>
                            <input
                                type="password"
                                name="confirmNewPassword"
                                class="form-control"
                                id="confirmNewPassword"
                                minlength="8"
                                maxlength="20"
                                placeholder="**********"
                                v-model="confirmNewPassword"
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
import { mapActions, mapGetters } from "vuex";
import { Modal } from "bootstrap";
import axios from "axios";
import { REMOTE_URL } from "@/constants/constant";
export default {
    name: "UpdateDetailsModal",
    data() {
        return {
            oldPassword: null,
            newPassword: null,
            confirmNewPassword: null,
        };
    },
    computed: {
        ...mapGetters(["user"]),
        currentUser() {
            let user = this.user;
            return { ...user };
        },
    },
    methods: {
        ...mapActions(["set_loader", "set_user", "set_toast_message"]),
        submitForm(e) {
            var empty = "Must Not Be Empty";
            var notMatch = "Password Not Matching";
            let forms = e.target;

            let currentPassword = this.oldPassword;
            let newPassword = this.newPassword;
            let confirmNewPassword = this.confirmNewPassword;

            console.log(
                newPassword &&
                    confirmNewPassword &&
                    newPassword === confirmNewPassword
            );
            if (currentPassword) {
                if (
                    !(
                        newPassword &&
                        confirmNewPassword &&
                        newPassword === confirmNewPassword
                    )
                ) {
                    if (!newPassword || !confirmNewPassword) {
                        if (!newPassword) {
                            forms["newPassword"].classList.add("is-invalid");
                            forms["newPassword"].setCustomValidity(
                                "Empty Not Valid"
                            );
                            forms["newPassword"].parentElement.querySelector(
                                ".invalid-feedback"
                            ).innerHTML = empty;
                        }
                        if (!confirmNewPassword) {
                            forms[
                                "confirmNewPassword"
                            ].parentElement.querySelector(
                                ".invalid-feedback"
                            ).innerHTML = empty;
                            forms["confirmNewPassword"].classList.add(
                                "is-invalid"
                            );
                            forms["confirmNewPassword"].setCustomValidity(
                                "Empty Not Valid"
                            );
                        }
                    } else if (newPassword !== confirmNewPassword) {
                        forms["confirmNewPassword"].classList.add("is-invalid");
                        forms["confirmNewPassword"].setCustomValidity(
                            "Password not match"
                        );
                        forms["confirmNewPassword"].parentElement.querySelector(
                            ".invalid-feedback"
                        ).innerHTML = notMatch;
                    }

                    return;
                } else {
                    forms["newPassword"].classList.add("is-valid");
                    forms["newPassword"].setCustomValidity("");
                    forms["confirmNewPassword"].classList.add("is-valid");
                    forms["confirmNewPassword"].setCustomValidity("");
                    forms["newPassword"].parentElement.querySelector(
                        ".invalid-feedback"
                    ).innerHTML = "";
                    forms["confirmNewPassword"].parentElement.querySelector(
                        ".invalid-feedback"
                    ).innerHTML = "";
                }
            }

            forms.classList.add("was-validated");
            if (!forms.checkValidity()) {
                return;
            }
            let data = {
                name: this.currentUser.username,
                role: this.currentUser.role,
                mobile_number:this.currentUser.mobile_number,
                currentPassword,
                newPassword,
                confirmNewPassword,
            };
            this.set_loader(true);
            console.log(data);
            axios
                .put(REMOTE_URL + "user", data, {
                    headers: {
                        "Auth-Token": localStorage.getItem("auth_token"),
                        "Content-type": "application/json",
                    },
                })
                .then((res) => {
                    console.log(res);
                    if (res.data.error_code) {
                        throw Error(res.data.error_message);
                    }
                    this.set_user(true);
                    forms.classList.remove("was-validated");
                    var modal = Modal.getInstance(
                        document.querySelector("#updateProfile")
                    );
                    modal.hide();
                    this.set_loader(false);
                })
                .catch((err) => {
                    this.set_toast_message(err);
                    this.set_loader(false);
                });
        },
    },
    beforeUnmount() {
        let elm = document.querySelector("#updateProfile");
        if (elm) {
            let modal = Modal.getInstance(elm);
            if (modal) {
                modal.hide();
            }
        }
    },
};
</script>

<style scoped>
.modal-dialog{
    max-width: 800px;
}
.flex-wrap{
    flex-wrap:wrap !important;
}
form {
    margin: 0;
    padding: 0 !important;
}
form .input-field.col {
    padding-left: 0 !important;
}
form .input-field.col label {
    left: 0;
}
</style>