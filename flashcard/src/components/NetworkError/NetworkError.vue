<template>
    <div
        class="modal fade"
        id="network_error"
        aria-labelledby="updateProfileLabel"
        aria-hidden="true"
        tabindex="-1"
    >
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <h1>Network Error</h1>
                <img src="../../assets/network_error.png" alt="Success!">
                <p>Please check your connection.</p>
            </div>
        </div>
    </div>
</template>

<script>
import {Modal} from 'bootstrap'
export default {
    name:"network_error",
    mounted(){
        var elem;
        var interval = setInterval(() => {
            elem = document.querySelector('.modal#network_error');
            if(elem){
                clearInterval(interval)
                var instance = new Modal(elem, {
                    keyboard:false,
                    backdrop:'static'
                });
                instance.show();
            }
        }, 10);
    },
    beforeUnmount(){
        var elm = document.querySelector('.modal#network_error');
        if (elm) {
            let modal = Modal.getInstance(elm);
            if (modal) {
                modal.hide();
            }
        }
    }
}
</script>

<style lang="scss" scoped>
.modal-content{
    border-radius: 50px;
    color: #2c3339;
    max-width: 450px;
    img{
        width:100%;
        height: 100%;
        max-height: 180px;
        object-fit: contain;
    }
    h1{
        font-size: 2.4rem;
        font-family: Poppins Bold;
        font-weight: 600;
        text-align: center;
    }
    p{
        font-size: 1.4rem;
        font-family: Poppins Regular;
        text-align: center;
    }
    i{
        font-size: 1.2rem;
    }
}
</style>