
const set_loader = ({commit}, status)=>{
    commit('set_loader', status)
}

const set_toast_message = ({commit}, message)=>{
    commit('set_toast_message', message)
}

const set_error_message = ({commit}, err)=>{
    if(err.response && err.response.data){
        if(err.response.data.error_message)
            err = err.response.data.error_message
        else if(err.response.data.message)
            err = err.response.data.message
        else if(err.response.data.response)
            err = err.response.data.response.error
    }
    commit('set_toast_message', err)
}

export default{
    set_loader,
    set_toast_message,
    set_error_message,
}