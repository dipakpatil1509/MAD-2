
const set_loader = (state, status) =>{
    state.loader = status;
}

const set_toast_message = (state, message) =>{
    state.toastMessage = message;
}

export default {
    set_loader,
    set_toast_message
};