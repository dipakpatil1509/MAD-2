<template>
    <div
        class="modal fade"
        id="webhooks"
        aria-labelledby="webhooksLabel"
        aria-hidden="true"
        tabindex="-1"
    >
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Webhooks</h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <form
                    name="webhooks"
                    class="needs-validation"
                    novalidate
                    @submit.prevent="submitForm"
                >
                    <div class="modal-body">
                        <div v-for="webhook, index in webhooks" :key="index">
                            <div class="mb-3">
                                <label :for="'webhook_' + index" class="form-label">Webhook {{index+1}}</label>
                                <input
                                    type="url"
                                    class="form-control"
                                    :id="'webhook_' + index"
                                    :name="'webhook_' + index"
                                    placeholder="Enter Webhook URL"
                                    v-model="webhook.url"
                                />
                                <div class="form-text">To delete, just leave it blank.</div>
                            </div>
                            <div class="mb-3">
                                <input
                                    class="form-check-input"
                                    type="checkbox"
                                    :name="'webhook_notify_' + index"
                                    :value="webhook.notify"
                                    v-model="webhook.notify"
                                    :id="'webhook_notify_' + index"
                                />
                                <label class="form-check-label" :for="'webhook_notify_' + index">
                                    Notify me when new public deck is created.
                                </label>
                            </div>
                        </div>
                        <button type="button" @click="add_more" class="btn btn-primary">
                            Add One More Webhook
                        </button>
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
import { mapActions } from "vuex";
import { Modal } from "bootstrap";
import axios from "axios";
import { REMOTE_URL, get_token } from "@/constants/constant";
export default {
    name: "WebhooksModal",
    data() {
        return {
            initial:{
                id:null,
                url:null,
                notify:false
            },
            webhooks:[],
        };
    },
    computed: {
    },
    methods: {
        ...mapActions(["set_loader", "set_toast_message", "set_error_message"]),
        add_more(){
            let last_hook = this.webhooks[this.webhooks.length - 1];
            if(last_hook && !last_hook.url){
                this.set_toast_message("Please add url");
                return;
            }
            this.webhooks.push({...this.initial})
        },
        submitForm(e) {
            
            let forms = e.target;
            forms.classList.add("was-validated");
            if (!forms.checkValidity()) {
                return;
            }
            let data = {
                "hooks":[...this.webhooks].filter(h=>h.url),
            };
            this.set_loader(true);
            console.log(data);
            let auth_token= get_token()
            axios.post(REMOTE_URL + "user/webhooks", data, {
                headers: {
                    "Auth-Token": auth_token,
                    "Content-type": "application/json",
                },
            }).then((res) => {
                console.log(res.data);
                if (res.data.error_code) {
                    throw Error(res.data.error_message);
                }
                if(res.data.data){
                    let flag = true;
                    res.data.data.forEach(item => {
                        if(!item.status){
                            flag = false;
                        }
                        this.set_toast_message(item.message);
                    });
                    if(flag){
                        forms.classList.remove("was-validated");
                        var modal = Modal.getInstance(
                            document.querySelector("#webhooks")
                        );
                        modal.hide();
                    }
                }
                this.set_loader(false);
            }).catch((err) => {
                this.set_error_message(err);
                this.set_loader(false);
            });
        },
        async get_webhooks(){
            try{
                let auth_token= get_token()
                let endpoint = "user/webhooks"
                const res = await axios.get(REMOTE_URL + endpoint, {
                    headers:{
                        "Auth-Token":auth_token,
                        "Content-type":"application/json"
                    }
                })
                this.webhooks = res.data;
                console.log(res.data);
            }catch (e){
                this.set_error_message(e)
            }
            if(this.webhooks.length === 0){
                this.webhooks.push({...this.initial})
            }
        }
    },
    watch:{
    },
    created(){
        this.get_webhooks()
    },
    beforeUnmount() {
        let elm = document.querySelector("#webhooks");
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
form {
    margin: 0;
    padding: 0 !important;
}

form input[type="checkbox"] + label {
    text-transform: none !important;
    font-size: 1.1rem;
    margin-left: 5px;
}
</style>