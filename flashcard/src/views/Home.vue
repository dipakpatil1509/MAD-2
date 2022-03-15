<template>
    <div id="deck">
    <div class="container deckDetails">
        <Decks />
    </div>
</div>
</template>

<script>
import Decks from "@/components/Home/Decks"
export default {
    name: "Home",
    components: {
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
