<template>
    <div id="loginPage" class="loginPage">
        <div class="container shadow-lg">
            <div class="row">
                <div class="col-lg-6 col-md-12 d-flex align-items-center">
                    <div class="loginContainer m-auto">
                        <router-link to="/" tabindex="-1">
                            <img src="@/assets/Logo.png" alt="FlashCard">
                        </router-link>
                        <h1>{{ isRegister ? "Register" : "Login"}} To FlashCard</h1>
                        <form class="needs-validation" novalidate @submit.prevent="loginSubmit">
                            <div v-if="isRegister" class="mb-3 has-validation">
                                <label for="name" class="form-label">Enter your name</label>
                                <input type="text" class="form-control" id="name" v-model="name" 
                                    name="name" placeholder="ABC XYZ" required>
                                <div class="invalid-feedback">
                                    Please enter valid name
                                </div>
                            </div>
                            <div class="mb-3 has-validation">
                                <label for="exampleInputEmail1" class="form-label">Email address</label>
                                <input type="email" class="form-control" id="exampleInputEmail1" v-model="email"
                                    aria-describedby="emailHelp" name="email" placeholder="abcd@abcd.com" required>
                                <div class="invalid-feedback">
                                    Please enter valid email address
                                </div>
                                <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                            </div>
                            <div class="mb-3">
                                <label for="exampleInputPassword1" class="form-label">Password</label>
                                <input type="password" name="pass" class="form-control" id="exampleInputPassword1" v-model="password"
                                    minlength="8" maxlength="20" placeholder="**********" required>
                                <div class="invalid-feedback">
                                    Please enter valid password
                                    Must be 8-20 characters long.
                                </div>
                            </div>
                            <div class="mb-0 form-check">
                              <input type="checkbox" name="remember" :value="true" v-model="remember" class="form-check-input" id="exampleCheck1">
                              <label class="form-check-label" for="exampleCheck1">Remember me</label>
                            </div>
                            <button type="submit" class="btn">Submit</button>
                        </form>
                        <router-link v-if="!isRegister" :to="{name:'Register', query:$route.query}">
                            Already a user? Login here
                        </router-link>
                        <router-link v-else :to="{name:'Login', query:$route.query}">
                            Not a user? Sign up for free
                        </router-link>
                        <div class="contactUs">
                            <p>Feel Free To Contact Us</p>
                            <a href="mailto:21f1004451@student.onlinedegree.iitm.ac.in">
                                <i class="fa fa-envelope" aria-hidden="true"></i>
                                21f1004451@student.onlinedegree.iitm.ac.in
                            </a>
                            <a class="contact" href="tel:+917447522900">
                                <i class="fa fa-phone" aria-hidden="true"></i>
                                +91 7447522900
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 d-lg-flex d-md-none d-sm-none d-none">
                    <div class="image">
                        <img src="@/assets/login_container_compress.webp" alt="FlashCard">
                    </div>
                </div>
            </div>
        </div>
        <div v-if="loading" class="loader_div_fixed mid">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>
</template>

<script>
import { REMOTE_URL } from '@/constants/constant.js'
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
    name:"Login",
    data(){
        return{
            email:"",
            password:"",
            name:"",
            remember:true,
            isRegister:false,
            loading:false
        }
    },
    methods:{
        ...mapActions([
            "set_toast_message"
        ]),
        loginSubmit(event){
            let form = event.target;
            form.classList.add('was-validated')
            if (!form.checkValidity()) {
                return false
            }

            if(8 > this.password.length || this.password.length > 15){
                this.set_toast_message("Please give correct password")
                return
            }
            if(this.email.length === 0){
                this.set_toast_message("Please give correct email")
                return
            }

            let data = {
                email:this.email,
                password:this.password,
                "remember":this.remember,
                name:this.name,
            }
            let endpoint = "login?include_auth_token"
            if (this.isRegister){
                endpoint = "register?include_auth_token";
            }

            this.loading = true;
            axios.post(REMOTE_URL + endpoint, data).then(res=>{
                if(res.data.response && res.data.response.user){
                    let auth_token = res.data.response.user.authentication_token;
                    localStorage.setItem('auth_token', auth_token);
                    this.loading = false;
                    this.$router.push(this.$route.query.next || "/" )
                }
                this.loading = false;
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
    },
    watch:{
        '$route':{
            handler(val){
                this.isRegister = val.name === "Register"
            },
            immediate:true
        }
    },
    mounted(){
        
    }
}
</script>
<style scoped>
.loginPage{
    height: 100vh;
    overflow: hidden;
    width: 100%;
    background-image: url("../../assets/login.png");
    background-position: center;
    background-repeat: no-repeat;
    background-size: 100% 100%;
    background-attachment: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 50px 0;
    margin-top: -100px;
    font-family: var(--font-regular);
}
.loginPage .container{
    height: 100%;
    width: 100%;
    background: #fff;
    padding: 0 !important;
    display: grid;
    grid-auto-flow: column;
    border-radius: 10px;
    overflow-y: auto;
}
.loginPage .container .row{
    margin: 0 !important;
}
.loginPage .container .image img{
    height: 100%;
    width: 100%;
    object-fit: contain;
    user-select: none;
    -webkit-user-select:none;
}
.loginContainer{
    text-align: center;
}
.loginContainer h1{
    margin:10px auto;
    font-size: 2rem;
    font-family: Poppins Bold, sans-serif;
}
.loginContainer img{
    width:100%;
    height: 100%;
    max-width: 70px;
    max-height: 70px;
    object-fit: contain;
}

.loginContainer form{
    text-align: left;
}
.loginContainer .btn{
    background: var(--theme);
    color: var(--white);
    font-size: 1.2rem;
    font-family: Poppins Medium, sans-serif;
    width: 100%;
    height: auto;
    padding: 5px;
    margin:10px auto;
}
.loginContainer .btn:hover, .loginContainer .btn:focus{
    background: var(--theme);
}
.loginContainer form{
    margin-top:15px;
}
.loginContainer .contactUs{
    margin:0 auto;
    margin-top:20px;
    width:100%;
}
.loginContainer .contactUs p{
    font-size: 1rem;
    font-family: Poppins Medium, sans-serif;
}
.loginContainer .contactUs a.contact{
    font-size: 1rem;
    color: var(--black);
    text-decoration: none;
    font-family: Poppins Medium, sans-serif;
    display: block;
    margin:5px 0 !important;
}

.loginContainer .contactUs a:focus{
    text-decoration: none;
}
.loginContainer .contactUs a i{
    font-size: 1.2rem;
    color: var(--black);
    margin-right:10px;
}
.loginContainer .contactUs a:hover, .loginContainer .contactUs a:hover i{
    color: var(--theme);
}
.tagLine{
    font-size:1rem;
    color:var(--theme);
    cursor:pointer;
    text-align:left;
}

@media screen and (max-width:768px){
    .loginPage{
        min-height: 100vh;
        height: 100%;
        overflow-x: hidden;
        overflow-y: auto;
        display: block;
    }
    .loginPage .container{
        height: 100%;
        width: 100%;
        padding: 15px !important;
        overflow-y: auto;
        overflow-x: hidden;
    }
    .loginPage .container .col{
        height: 100%;
        margin:0;
    }
    .loginContainer img{
        max-width: 130px;
        max-height: 65px;
    }
    .loginContainer h1{
        margin:10px auto;
        font-size: 1.8rem;
    }
}

@media screen and (max-width: 568px){
    .loginPage{
        background-image: url("/media/login_mobile.png");
    }
    .loginContainer .contactUs a i{
        margin-right:5px;
        margin-left: 5px;
    }
    .mobile_number p, p.counter{
        font-size: 1.25rem;
        margin-top:12px;
    }
    p.counter{
        font-size: 1rem;
        margin-top:16px;
    }
}

@media screen and (max-height: 600px){
    .loginContainer .contactUs{
        margin-top:10px;
    }
    .input-field{
        margin:0 auto;
    }
}

@media screen and (max-width: 320px){
    .loginContainer .contactUs a, .loginContainer .contactUs a i{
        font-size: 1rem;
    }
    .loginContainer .contactUs p.nameAndIcons{
        text-align: center !important;
    }
    .loginContainer .contactUs a{
        display: block;
    }
    .loginContainer .contactUs span.icons{
        float:none !important;
    }
    .loginContainer .contactUs span.icons a{
        display: inline-block;
    }
    .mobile_number label{
        margin-left:13% !important;
    }
    .mobile_number input{
        width:87% !important;
        margin-left:13% !important;
    }
    .loginContainer .contactUs a.contact{
        font-size: 1.1rem;
    }
}
</style>