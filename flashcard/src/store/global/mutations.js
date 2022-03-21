
const set_loader = (state, status) =>{
    state.loader = status;
}

const set_toast_message = (state, message) =>{
    if(message){
        state.toastMessage.push(message);
        setTimeout(() => {
            state.toastMessage= state.toastMessage.slice(1) || []
        }, 6000);
    }
    else if(state.toastMessage.length > 0)
        state.toastMessage = state.toastMessage.slice(1) || []
}

export default {
    set_loader,
    set_toast_message
};