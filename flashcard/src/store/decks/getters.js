const decks = (state) => {
    return state.decks
};

const current_deck= (state) => {
    return state.current_deck
};

const current_card= (state) => {
    return state.current_card
};
const current_response= (state) => {
    return state.current_response
};

export default {
    decks,
    current_deck,
    current_card,
    current_response,
}