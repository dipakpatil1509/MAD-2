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
                        name: 'Result',
                        params: { response_id: final.id },
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
                        Averge time :- {{ get_time(final.avg_time) }} sec
                    </h3>
                </div>
                <div class="completed_at">
                    <h3 class="fs-6">
                        Completed At :- {{ final.completed_at }}
                    </h3>
                </div>
            </div>
        </div>

        <div
            v-if="final.cards && final.cards.length > 0"
            class="question_type"
        >
            <ul>
                <li
                    v-for="(value, key) in diff_count"
                    :key="key"
                    :class="key"
                >
                    {{ key }} - {{ value }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: "FinalDeck",
    props: ["final"],
    data(){
        return {
            diff_count:{}
        }
    },
    methods:{
        get_count(diff){
            if(!this.diff_count[diff])
                this.diff_count[diff] = 0
            this.diff_count[diff] += 1
        },
        get_time(time){
            if(time > 0){
                var minutes = Math.floor(time / 60000);
                var seconds = ((time % 60000) / 1000).toFixed(0);
                return (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00"
        }
    },
    watch:{
        final:{
            handler(val){
                console.log(val);
                if(val && val.cards.length > 0){
                    val.cards.forEach(item=>{
                        this.diff_count = {}
                        this.get_count(item.difficulty)
                    })
                }
            },
            immediate:true
        }
    },
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