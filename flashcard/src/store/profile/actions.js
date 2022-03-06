import axios from "axios"
import { REMOTE_URL } from "../../constants/constant"

const set_user = async ({commit})=>{
    let user = null;
    try{
        let auth_token= localStorage.getItem('auth_token');
        if (!auth_token) {
            throw Error("Please login to continue")
        }
        const res = await axios.get(REMOTE_URL + "user", {
            headers:{
                "Auth-Token":auth_token,
                "Content-type":"application/json"
            }
        })
        console.log(res.data);
        user = res.data;
    }catch (e){
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