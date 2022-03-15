import axios from "axios"
import { get_token, REMOTE_URL } from "../../constants/constant"

const set_decks = async ({commit, dispatch}, flag=0)=>{
    let decks = [];
    try{
        let auth_token= get_token()
        let endpoint = "decks" + "?flag=" + flag
        const res = await axios.get(REMOTE_URL + endpoint, {
            headers:{
                "Auth-Token":auth_token,
                "Content-type":"application/json"
            }
        })
        if(res.data.error_code){
            throw Error(res.data.error_message)
        }
        decks = res.data;
        console.log(decks);
    }catch (e){
        dispatch('set_error_message', e)
    }
    commit('set_decks', decks)
}

const set_current_deck = async ({commit}, deck_id)=>{
    let deck = null;
    if(deck !== undefined){
        try{
            let auth_token= get_token()
            let endpoint = "deck/" + deck_id
            const res = await axios.get(REMOTE_URL + endpoint, {
                headers:{
                    "Auth-Token":auth_token,
                    "Content-type":"application/json"
                }
            })
            if(res.data.error_code){
                throw Error(res.data.error_message)
            }
            deck = res.data;
            console.log(deck);
        }catch (err){
            commit('set_error_message', err)
        }
    }
    commit('set_current_deck', deck)
}

const set_current_card = async ({commit}, card_id)=>{
    let card = null;
    if(card_id !== undefined){
        try{
            let auth_token= get_token()
            let endpoint = "card/" + card_id
            const res = await axios.get(REMOTE_URL + endpoint, {
                headers:{
                    "Auth-Token":auth_token,
                    "Content-type":"application/json"
                }
            })
            if(res.data.error_code){
                throw Error(res.data.error_message)
            }
            card = res.data;
            console.log(card);
        }catch (err){
            commit('set_error_message', err)
        }
    }
    commit('set_current_card', card)
}


const set_current_response = async ({commit}, response_id)=>{
    let response = null;
    if(response_id !== undefined){
        try{
            let auth_token= get_token()
            let endpoint = "review/" + response_id
            const res = await axios.get(REMOTE_URL + endpoint, {
                headers:{
                    "Auth-Token":auth_token,
                    "Content-type":"application/json"
                }
            })
            if(res.data.error_code){
                throw Error(res.data.error_message)
            }
            response = res.data;
            console.log(response);
        }catch (err){
            commit('set_error_message', err)
        }
    }
    commit('set_current_response', response)
}


export default{
    set_decks,
    set_current_deck,
    set_current_card,
    set_current_response,
}