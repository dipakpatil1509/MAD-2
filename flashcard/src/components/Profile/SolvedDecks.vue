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
            </tr>
        </thead>
        <tbody class="fs-6">
            <tr v-for="(item, index) in decks" :key="index">
                <th scope="row">1</th>
                <td style="text-align: left">
                    <router-link
                        :to="{
                            name: 'ViewDeck',
                            params: { deck_id: item.deck.id },
                        }"
                        class="fs-6 mt-0"
                    >
                        {{ item.deck.name }}
                    </router-link>
                </td>
                <td>{{ item.deck.created_for.name }}</td>
                <td>{{ item.score }}</td>
                <td>{{ item.avg_time }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name:"SolvedDecks",
    props:["decks"]
};
</script>

<style scoped>
</style>