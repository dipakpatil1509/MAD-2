import axios from "axios"
import { createDP, REMOTE_URL } from "../../constants/constant"

const set_user = async ({commit}, isAll=false)=>{
    let user = null;
    try{
        let auth_token= localStorage.getItem('auth_token');
        if (!auth_token) {
            throw Error("Please login to continue")
        }
        let endpoint = "user"
        if(isAll){
            endpoint += "?isAll=1"
        }
        const res = await axios.get(REMOTE_URL + endpoint, {
            headers:{
                "Auth-Token":auth_token,
                "Content-type":"application/json"
            }
        })
        user = res.data;
        user.image = createDP(user.username || "F C")
    }catch (e){
        localStorage.removeItem('auth_token');
        let msg = e
        if(e.response && e.response.data && e.response.data.response){
            msg = e.response.data.response.error
        }
        commit('set_toast_message', msg)
    }
    commit('set_user', user)
}

export default{
    set_user,
}