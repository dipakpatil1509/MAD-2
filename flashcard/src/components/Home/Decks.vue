<template>
    <h1 class="headline">
        Decks
        <button
            data-bs-toggle="modal"
            data-bs-target="#create_a_deck"
            class="btn translate-middle-y updateProfile float-end"
        >
            Create a Deck
        </button>
    </h1>
    <div class="sort_options">
        <div class="sorts">
            <div class="sort_title shadow">
                Filter <i class="fas fa-chevron-right"></i>
            </div>
            <div class="option">
                <input type="radio" name="sort" id="public" value="0" 
                    v-model="currentFilter" hidden />
                <label for="public" class="shadow">
                    <span>Public</span>
                </label>
            </div>
            <div class="option">
                <input type="radio" name="sort" id="role" value="1" 
                    v-model="currentFilter" hidden />
                <label for="role" class="shadow">
                    <span>{{ role }}</span>
                </label>
            </div>
            <div class="option">
                <input type="radio" name="sort" id="user" value="2" 
                    v-model="currentFilter" hidden />
                <label for="user" class="shadow">
                    <span>My Decks</span>
                </label>
            </div>
            <div class="option">
                <input type="radio" name="sort" id="myUnpublish" value="3"
                    v-model="currentFilter" hidden />
                <label for="myUnpublish" class="shadow">
                    <span>My Unpublish</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="deckRow">
        
        <router-link v-for="(item, index) in decks" :key="index"
            :to="{ name: 'ViewDeck', params:{deck_id:item.id} }" 
            class="container bg-white mb-3 d-flex align-items-center deck justify-content-between">
            <div>
                <h1>
                    {{ item.name }}
                </h1>
                <p>
                    For
                    {{ item.created_for ? item.created_for : 'All' }}
                </p>
            </div>
            <div class="right-text">
                <p>
                    {{ item.number_of_cards }}
                </p>
                <h6>
                    ~By {{ item.user.username || item.user.email }}
                </h6>
                <p class="small text-secondary ">At {{ new Date(item.created_at).toLocaleString('en-In') }}</p>
            </div>
        </router-link>
        <div v-if="decks.length === 0" class="deckRow text-center">
            <h1 class="fs-4">No Deck Found!</h1>
        </div>
    </div>
    <CreateDeck @get_decks="get_decks" />
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import CreateDeck from '@/components/Home/CreateDeck';
export default {
    name:"HomeDecks",
    data(){
        return{
            currentFilter:0,
        }
    },
    components: {
		CreateDeck,
	},
    computed:{
        ...mapGetters(["user", "decks"]),
        role(){
            let role = this.user.role;
            return role && role.charAt(0).toUpperCase() + role.slice(1).toLowerCase();
        }
    },
    methods:{
        ...mapActions(["set_decks", "set_loader"]),
        get_decks(){
            this.set_loader(true)
            this.set_decks(this.currentFilter).then(()=>{
                this.set_loader(false)
            });
        }
    },
    watch:{
        currentFilter:{
            handler:function() {this.get_decks()},
            immediate:true,
        }
    }
};
</script>

<style scoped>
a{
    text-decoration: none;
}
.right-text{
    text-align: right;
}
.deckRow .container{
    padding: 10px 20px;
}
.deckRow h1{
    font-size: 1.3rem;
    font-family: var(--font-medium);
    margin-bottom: 5px;
}
h6{
    font-size: 0.95rem;
    font-family: var(--font-medium);
    margin-bottom: 0;
}
.btn.updateProfile, .btn.logout{
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
    margin-top: 25px;
}
.btn.logout {
    border: var(--black) 1px solid;
    background:var(--white);
    color:#222;
}


.sort_options{
    margin: 45px 0 25px;
    position: relative;
    display: block;
}
.sorts{
    display: inline-flex;
    flex-wrap: wrap;
    align-items: flex-start;
    column-gap: 15px;
    row-gap: 15px;
    max-width: max-content;
}
.sort_title{
    font-size: 1.2rem;
    font-family: var(--font-medium);
    background: var(--buttonColor);
    color: var(--white);
    padding: 5px 15px;
    min-width: 170px;
    display: flex;
    align-items: center;
    border-radius: 150px;
}
.sort_title i{
    margin:0 0 0 auto;
}
.option label{
    font-size: 1.1rem;
    font-family: var(--font-medium);
    color: var(--active-color);
    background: var(--white);
    padding: 5px 25px;
    min-width: 150px;
    display: flex;
    align-items: center;
    border-radius: 150px;
    cursor: pointer;
    text-transform: capitalize;
}

.sort_options input[type="radio"]:checked + label{
    background: var(--buttonColor);
    color: var(--white);
}
</style>