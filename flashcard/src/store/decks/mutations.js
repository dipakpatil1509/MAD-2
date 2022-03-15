
const set_decks = (state, decks) =>{
    state.decks = decks;
}

const set_current_deck = (state, current_deck) =>{
    state.current_deck = current_deck;
}

const set_current_card = (state, current_card) =>{
    state.current_card = current_card;
}

const set_current_response = (state, current_response) =>{
    state.current_response = current_response;
}


export default {
    set_decks,
    set_current_deck,
    set_current_card,
    set_current_response,
};