
const set_loader = ({commit}, status)=>{
    commit('set_loader', status)
}

const set_toast_message = ({commit}, message)=>{
    commit('set_toast_message', message)
}

export default{
    set_loader,
    set_toast_message
}