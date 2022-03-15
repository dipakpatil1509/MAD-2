import axios from "axios"
import { createDP, get_token, REMOTE_URL } from "../../constants/constant"

const set_user = async ({commit}, isAll=false)=>{
    let user = null;
    try{
        let auth_token= get_token()
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
        commit('set_error_message', e)
    }
    commit('set_user', user)
}

export default{
    set_user,
}