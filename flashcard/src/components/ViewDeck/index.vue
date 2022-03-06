<template>
    <div id="deck">
        <div class="container deckDetails">
            <div v-if="deck">
                <h1 class="headline">
                    {{ deck.name }}
                    <div class="float-end">
                        <!-- deck.created_by_id == user.id -->
                        <div v-if="true">
                            <a
                                onclick="return confirm('Are you sure you want to delete?')"
                                href="{{url_for('deck.delete_deck', deck_id=deck.id) }}"
                                class="btn updateProfile btn-secondary d-inline-block float-end"
                            >
                                Delete Deck
                            </a>
                            <a
                                href="{{url_for('card.add_card', deck_id=deck.id) }}"
                                class="btn me-3 mb-3 updateProfile d-inline-block float-end"
                            >
                                Add Card
                            </a>
                            <button
                                data-bs-toggle="modal"
                                data-bs-target="#create_a_deck"
                                class="btn updateProfile mb-3 me-3 d-inline-block"
                            >
                                Update Deck
                            </button>
                        </div>
                        <a
                            v-if="cards && cards.length > 0"
                            href="#!"
                            @click.prevent="download_excel"
                            class="btn ms-auto me-0 updateProfile h-50"
                        >
                            Download Cards as Excel
                        </a>
                    </div>
                </h1>
                <div class="deckRow">
                    <div
                        class="
                            container
                            bg-white
                            mb-3
                            d-flex
                            align-items-center
                            deck
                            justify-content-between
                        "
                    >
                        <div>
                            <h1>
                                {{ deck.name }}
                            </h1>
                            <p>
                                For
                                {{
                                    deck.created_for ? deck.created_for : "All"
                                }}
                            </p>
                        </div>
                        <div class="right-text">
                            <p>
                                {{ deck.number_of_cards }}
                            </p>
                            <h6>~By {{ deck.user && deck.user.name }}</h6>
                            <p class="small text-secondary">
                                At {{ deck.created_at }}
                            </p>
                        </div>
                    </div>
                </div>

                <a v-if="cards && cards.length > 0"
                    href="{{ url_for('review.review_form', deck_id=deck.id) }}"
                    class="btn updateProfile mb-5 mt-5 mx-auto d-block w-25 p-2 fs-4"
                >
                    Start Test
                </a>
                <h6 v-else>No Questions Added</h6>
                <div v-if="deck.created_by_id == user.id" class="container">
                    <div class="mb-5 d-flex align-items-end">
                        <form
                            class="w-50 ms-0"
                            action="{{ url_for('card.import_card', deck_id=deck.id) }}"
                            enctype="multipart/form-data"
                            method="POST"
                        >
                            <h6>Upload Excel</h6>
                            <div class="input-group">
                                <input
                                    type="file"
                                    class="form-control"
                                    id="file"
                                    aria-describedby="file"
                                    aria-label="Upload"
                                    required
                                    name="importFile"
                                    accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, .xlsx, .xls"
                                />
                                <button
                                    class="btn btn-secondary"
                                    type="submit"
                                    id="file"
                                >
                                    Upload
                                </button>
                            </div>
                        </form>

                        <a
                            v-if="cards && cards.length > 0"
                            href="{{ url_for('card.download_excel', deck_id=deck.id) }}"
                            class="btn ms-auto me-0 updateProfile h-50"
                        >
                            Download Cards as Excel
                        </a>
                    </div>
                    <create-deck :isUpdate="true" :deck="{}" />
                    <div class="row">
                        <div
                            v-for="(card, index) in cards || []"
                            :key="index"
                            class="
                                mb-3
                                card
                                col-lg-4 col-md-4 col-sm-6 col-xs-12
                            "
                        >
                            <div class="card-body" style="min-height: 8em">
                                <h1 class="fs-5">{{ card.front }}</h1>
                            </div>
                            <div class="card-footer bg-transparent">
                                <a
                                    href="{{ url_for('card.edit_card', card_id=card.id) }}"
                                    class="btn mb-2 updateProfile d-block"
                                >
                                    Edit Card
                                </a>
                                <a
                                    onclick="return confirm('Are you sure you want to delete?')"
                                    href="{{ url_for('card.delete_card', card_id=card.id, deck_id=deck.id) }}"
                                    class="
                                        btn
                                        updateProfile
                                        btn-secondary
                                        d-block
                                    "
                                >
                                    Delete Card
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="deckRow text-center">
                <h1 class="">No Deck Found!</h1>
                <p class="text-secondary">Please check id</p>
            </div>
        </div>
    </div>
</template>

<script>
import CreateDeck from "../Home/CreateDeck.vue";
export default {
    components: { CreateDeck },
    name: "ViewDeck",
    data() {
        return {
            deck: {},
            cards: [],
            user:{}
        };
    },
    computed: {},
    methods: {
        download_excel() {
            // {{ url_for('card.download_excel', deck_id=deck.id) }}
        },
    },
};
</script>

<style scoped>
#deck{
    position: relative;
    height: 100%;
}
#deck .container{
    padding:10px 15px;
    background: var(--backgroundColor);
}
#deck .deckDetails{
    max-width:70%;
    margin-bottom: 100px;
}
.right-text{
    text-align: right;
}
.deck h1{
    font-size: 1.3rem;
    font-family: var(--font-medium);
    margin-bottom: 5px;
}
.deck h6{
    font-size: 0.95rem;
    font-family: var(--font-medium);
    margin-bottom: 0;
}
.btn.updateProfile{
    border: var(--buttonColor) 1px solid;
    background:var(--buttonColor);
    border-radius: 50px;
    color:white;
    font-size:1.1rem;
    height: auto;
    padding: 2px 25px;
    font-family: Poppins Regular, sans-serif;
    cursor: pointer;
    text-transform: capitalize;
}
.btn.updateProfile.btn-secondary{
    color: #fff;
    background-color: #6c757d;
    border-color: #6c757d;
}


</style>