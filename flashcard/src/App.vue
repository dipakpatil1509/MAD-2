<template>
    <Navbar v-if="!hideNavFooter.includes($route.name)" />
    <main class="mainDiv">
        <div aria-live="polite" aria-atomic="true"
            class="toast_container"
        >
            <div v-for="toast, index in toastMessage" :key="index" 
                class="toast fade show"  role="alert" 
                :id="'toast_' + index" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <strong class="me-auto">
                        {{ toast }}
                    </strong>
                    <button
                        type="button" class="btn-close"
                        data-bs-dismiss="toast" aria-label="Close"
                    ></button>
                </div>
            </div>
        </div>
        <router-view />
    </main>
    <Footer v-if="!hideNavFooter.includes($route.name)" />
	<div v-if="loader" class="loader_div_fixed mid">
		<div class="spinner-border" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
</template>

<script>
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { mapActions, mapGetters } from 'vuex'
export default {
    name: "App",
    components: {
        Navbar,
        Footer,
    },
    data() {
        return {
			hideNavFooter:["Login", "Register"],
        };
    },
	computed:{
		...mapGetters([
            "loader",
            "toastMessage"
        ])
	},
	methods:{
        ...mapActions([
            "set_toast_message",
            "set_user"
        ]),
	},
	watch:{
	},
	mounted(){
        window.onstorage =  function(e) {
            if(e.key === "auth_token"){
                this.set_user({isAll:false, isLogout:false})
            }
        };
	}
};
</script>

<style lang="scss">
@font-face {
    font-family: Poppins Bold;
    src: url("./assets/Poppins/Poppins-Bold.ttf");
}
@font-face {
    font-family: Poppins Regular;
    src: url("./assets/Poppins/Poppins-Regular.ttf");
}
@font-face {
    font-family: Poppins Medium;
    src: url("./assets/Poppins/Poppins-Medium.ttf");
}

* {
    margin: 0;
    padding: 0;
}
:root {
    --black: #444;
    --white: #ffffff;
    --theme: #6642e4;
    --themeDark: #7b13fa;
    --buttonColor: #dc3c4d;
    --buttonColorRGB: rgb(220, 60, 77);
    --backgroundColor: #f5f5ef;
    --font-regular: Poppins Regular, sans-serif;
    --font-medium: Poppins Medium, sans-serif;
    --font-bold: Poppins Bold, sans-serif;
}
html {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}
body {
    min-height: 100vh;
    height: 100%;
    width: 100%;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-size: 15px;
    font-family: var(--font-regular);
    background: #fff;
    color: #444;
}
body::-webkit-scrollbar {
    display: none;
}

.toast_container{
    position:fixed;
    top: 10%;
    left: 0;
    width:100%;
    z-index: 13232355;
}

.toast_container .toast{
    display: block;
    margin: 10px auto;
    width:fit-content;
    max-width: 600px;
    height: auto;
    word-break: break-all;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}
p {
    margin: 0;
}
a {
    color: var(--black);
    text-decoration: none;
}

label {
    text-transform: uppercase;
    font-style: normal;
    font-family: Roboto Medium, Aria l;
}
input.invalid + label {
    color: #9e9e9e !important;
}
input.valid + label {
    color: var(--themeColor) !important;
    font-size: 1.2rem !important;
}
.input-field input.invalid {
    border-bottom: 1px solid #9e9e9e !important;
    box-shadow: none !important;
}
/* label underline focus color */
.input-field input:focus,
.input-field input.valid {
    border-bottom: 1px solid var(--themeColor) !important;
    box-shadow: 0 1px 0 0 var(--themeColor) !important;
}
::-moz-selection {
    /* Code for Firefox */
    color: #fff;
    background: var(--theme);
}

::selection {
    color: #fff;
    background: var(--theme);
}
.btn {
    font-family: Poppins Medium, sans-serif;
    font-size: 1.1rem;
}

.headline {
    font-size: 2.1rem;
    font-family: var(--font-bold), sans-serif;
    margin: 15px 0 25px;
    padding-bottom: 10px;
    position: relative;
}
.headline::after {
    position: absolute;
    content: "";
    bottom: 0px;
    left: 0px;
    height: 4px;
    width: 60px;
    background: -ms-linear-gradient(
        right,
        var(--themeDark) 0%,
        var(--theme) 100%
    );
    background: -moz-linear-gradient(
        right,
        var(--themeDark) 0%,
        var(--theme) 100%
    );
    background: -o-linear-gradient(
        right,
        var(--themeDark) 0%,
        var(--theme) 100%
    );
    background: -webkit-gradient(
        linear,
        left top,
        right top,
        color-stop(0, var(--themeDark)),
        color-stop(100, var(--theme))
    );
    background: -webkit-linear-gradient(
        right,
        var(--themeDark) 0%,
        var(--theme) 100%
    );
    background: linear-gradient(
        to right,
        var(--themeDark) 0%,
        var(--theme) 100%
    );
}
.mainDiv {
    min-height: calc(100vh - 40px);
    padding-top: 100px;
}
.loader_div_fixed,
.loader_div_absolute{
	position: fixed;
	top:0;
	left: 0;
	height: 100%;
	width: 100%;
	background: #fff;
	z-index:133132131;
	display: flex;
	align-items: center;
	justify-content: center;
}
.loader_div_absolute{
	position: absolute;
}
.mid{
	background: rgba($color: #fff, $alpha: 0.5);
}
.spinner-border{
	width: 50px !important;
	height: 50px !important;
	border-color:var(--theme) !important;
	border-right-color: transparent !important;
}
.spinner-border-sm{
	width: 15px !important;
	height: 15px !important;
}
</style>
