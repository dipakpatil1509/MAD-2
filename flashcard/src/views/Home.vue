<template>
    <div id="deck">
    <div class="container deckDetails">
        <Decks />
		<CreateDeck />
    </div>
</div>
</template>

<script>
import CreateDeck from '@/components/Home/CreateDeck'
import Decks from "@/components/Home/Decks"
export default {
    name: "Home",
    components: {
		CreateDeck,
		Decks
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
</style>
