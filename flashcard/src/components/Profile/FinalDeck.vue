<template>
    <h1 class="headline">Last Reviewed</h1>
    <div class="progress mt-3 w-75 mx-auto bg-danger" style="height: 25px">
        <div
            class="progress-bar bg-success"
            id="progressBar"
            role="progressbar"
            :style="'width:' + final.score + '%'"
        >
            {{ final.score }}%
        </div>
    </div>
    <div class="mx-auto d-block w-75">
        <div class="d-flex align-items-center w-100">
            <div class="mt-4">
                <router-link
                    v-if="final.deck"
                    :to="{
                        name: 'ViewDeck',
                        params: { deck_id: final.deck.id },
                    }"
                    class="fs-5"
                >
                    {{ final.deck.name }}
                </router-link>
                <a v-else href="#!" @click.prevent class="fs-5">Deleted Deck</a>
            </div>
            <div class="ms-auto me-0">
                <div class="avg_time mt-4">
                    <h3 class="fs-6">
                        Averge time :- {{ final.avg_time }} sec
                    </h3>
                </div>
                <div class="completed_at">
                    <h3 class="fs-6">
                        Completed At :- {{ final.completed_at }}
                    </h3>
                    <!-- .strftime(" %H:%M:%S, %d/%m/%Y") -->
                </div>
            </div>
        </div>

        <div
            v-if="final_decks && final_decks.length > 0"
            class="question_type"
        >
            <ul>
                <li
                    v-for="(item, index) in final_cards"
                    :key="index"
                    :class="item.difficulty.name"
                >
                    {{ item.difficulty.name }} - {{ item[1] }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: "FinalDeck",
    props: ["final", "final_decks"],
};
</script>

<style scoped>

.question_type ul{
    list-style-type: none;
    display: flex;
    justify-content: space-evenly;
    margin-top: 20px;

}
.question_type li{
    font-size: 1.4rem;
}
.question_type li::before{
    content: "";
    width:35px;
    height:35px;
    position: relative;
    display: inline-block;
    vertical-align: middle;
}
.Easy::before{
    background: seagreen;
}
.Moderate::before{
    background: yellowgreen;
}
.Hard::before{
    background: tomato;
}
</style>