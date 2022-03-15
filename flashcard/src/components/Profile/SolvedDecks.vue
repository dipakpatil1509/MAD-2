<template>
    <h1 class="headline">All Reviewed</h1>
    <table class="table text-center">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Tag</th>
                <th scope="col">Score</th>
                <th scope="col">Avg Time</th>
                <th scope="col">Completed at</th>
            </tr>
        </thead>
        <tbody class="fs-6">
            <tr v-for="(item, index) in decks" :key="index">
                <th scope="row">1</th>
                <td>
                    <router-link
                        :to="{
                            name: 'Result',
                            params: { response_id: item.id },
                        }"
                        class="fs-6 mt-0"
                    >
                        {{ item.deck.name }}
                    </router-link>
                </td>
                <td>{{ item.deck.created_for }}</td>
                <td>{{ item.score }}</td>
                <td>{{ get_time(item.avg_time) }} secs</td>
                <td>{{ new Date(item.completed_at).toLocaleString('en-In') }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name:"SolvedDecks",
    props:["decks"],
    methods:{
        get_time(time){
            if(time > 0){
                var minutes = Math.floor(time / 60000);
                var seconds = ((time % 60000) / 1000).toFixed(0);
                return (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            }
            return "00:00"
        }
    }
};
</script>

<style scoped>
a{
    color: #000;
    font-size: 1.1rem;
    font-weight: 600;
}
</style>