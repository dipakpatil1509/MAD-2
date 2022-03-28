<template>
    <h1 class="headline">Account Setting</h1>
    <div v-if="user" class="profileRow mb-5">
        <div class="image" align="center">
            <img :src="user.image" :alt="user.username" />
        </div>
        <div class="details">
            <h2>{{ user.username ? user.username : "Flashcard User" }}</h2>
            <a :href="'mailto:' + user.email" class="uniq_username">{{
                user.email
            }}</a>
            <p>{{ user.role }}</p>

            <button
                data-bs-toggle="modal"
                data-bs-target="#updateProfile"
                class="btn updateProfile"
            >
                Update Profile
            </button>
            <button
                data-bs-toggle="modal"
                data-bs-target="#webhooks"
                class="btn updateProfile mx-2"
            >
                Webhooks
            </button>
            <button class="btn logout" href="#!" :disabled="loading" @click.prevent="logout">
                <span v-if="loading" class="spinner-border spinner-border-sm" 
                role="status" aria-hidden="true"></span>
                <span v-else>Logout</span>
            </button>
            <br />
        </div>
        <div class="badge text-center">
            <div>
                <h1>
                    {{ user.review_response }}
                </h1>
                <p class="text-center">Average Score</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapActions, mapGetters } from 'vuex';
import {REMOTE_URL} from "@/constants/constant";
export default {
    name:"UserProfile",
    data(){
        return{
            loading:false
        }
    },
    computed:{
        ...mapGetters([
            "user"
        ])
    },
    methods:{
        ...mapActions([
            "set_toast_message", "set_user"
        ]),
        logout(){
            this.loading = true;
            axios.get(REMOTE_URL + "logout",{
                headers:{
                    "Auth-Token":localStorage.getItem('auth_token'),
                }
            }).then(res=>{
                console.log(res.data);
                localStorage.removeItem('auth_token');
                this.loading = false;
                this.set_user({isLogout:true})
                this.set_toast_message("Thank you! Please come back soon!")
                this.$router.push("/login")
            }).catch(err=>{
                console.log(err);
                if(err.response && err.response.data && err.response.data.response){
                    let errors = err.response.data.response.errors
                    Object.keys(errors).map(key=>{
                        let msg = key.toString().charAt(0).toUpperCase();
                        msg += key.slice(1);
                        msg += ": " + errors[key]
                        this.set_toast_message(msg)
                    })
                }else{
                    this.set_toast_message(err)
                }
                this.loading = false;
            })
        }
    }
};
</script>

<style scoped>
.profileRow{
    display: flex;
    position: relative;
    flex-wrap: wrap;
}
.image{
    background: #fff;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding:0;
    flex-basis:22%;
    height: auto;
    min-height: 220px;
}
img{
    max-width: 100%;
    max-height: 100%;
    height: auto;
    object-fit: contain;
}
div.details{
    padding:10px 25px;
    flex-basis:48%;
}
div.badge{
    flex-basis: 30%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding:0;
    position: relative;
    color: var(--black);
}

div.badge h1{
    font-size: 5rem;
}
h2{
    font-size: 1.7rem;
    font-family: var(--font-medium), sans-serif;
    font-weight: 600;
    margin: 15px 0 0;
    position: relative;
}
div.badge h2.count{
    position: absolute;
    top:0;
    bottom: 0;
    left: 0;
    right: 0;
    font-size: 6rem;
    font-family: Roboto Regular, sans-serif;
    margin: -15px 0 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
p,
a:not(.btn){
    font-size: 1.2rem;
    font-family: var(--font-regular), sans-serif;
    margin: 5px 0 0;
    position: relative;
    display: block;
}
.uniq_username{
    font-size: 1.1rem !important;
    color:lightslategray;
}
.btn.updateProfile, .btn.logout{
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
    margin-top: 25px;
}
.btn.logout {
    border: var(--black) 1px solid;
    background:var(--white);
    color:#222;
    min-width: 150px;
}

@media screen and (max-width:992px) {
    .btn.updateProfile, .btn.logout{
        margin-top: 10px;
    }
}

@media screen and (max-width:800px) {
    .image{
        flex-basis:100%;
        background: transparent;
    }
    .image img{
        border-radius: 50%;
    }
    div.details{
        flex-basis:70%;
    }
    div.badge{
        flex-basis: 30%;
    }
    div.badge h1{
        font-size: 3.5rem;
    }
}

@media screen and (max-width:600px) {
    .btn.updateProfile, .btn.logout{
        margin-left: 0 !important;
    }
}

@media screen and (max-width:500px) {
    
    div.details, div.badge{
        flex-basis:100%;
        text-align: center;
        width: 100%;
        word-break: break-all;
        padding: 10px;
    }
    .btn.updateProfile, .btn.logout{
        width: 100%;
        box-sizing: border-box;
    }
}
</style>