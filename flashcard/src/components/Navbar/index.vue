<template>
    <header id="baseHTML">
        <nav class="navbar fixed-top navbar-expand-lg">
            <div class="container">
                <router-link class="navbar-brand " :to="{ name: 'Home' }">
                    <img
                        src="../../assets/Logo.png"
                        alt=""
                        class="d-inline-block align-text-top"
                    />
                    FlashCard
                </router-link>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent"
                    aria-expanded="false"
                    aria-label="FlashCard Menu Toggle"
                >
                    <i class="navbar-toggler-icon fas fa-bars"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav d-flex ms-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'Home' }">
                                Decks
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'AddCard' }">
                                Add
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'Profile' }">
                                {{ user.name ? user.name : user.email || "Profile"}}
                            </router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
export default {
    name:"Navbar",
    data(){
        return{
            user:{}
        }
    },
    mounted(){}
};
</script>

<style scoped>

.navbar {
    background: var(--backgroundColor);
    -webkit-box-shadow: 0 2px 2px 0 rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%), 0 1px 5px 0 rgb(0 0 0 / 20%);
    box-shadow: 0 2px 2px 0 rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%), 0 1px 5px 0 rgb(0 0 0 / 20%);
}
.navbar a, .navbar-toggler{
    color: var(--theme);
}

.navbar-toggler-icon{
    width: auto;
    height: auto;
}
.navbar-toggler:focus{
    box-shadow: none;
}

.navbar-brand{
    display: flex;
    align-items: center;
    column-gap: 5px;
    font-family: var(--font-medium);
}
.navbar-brand img{
    width: 50px;
    height: 50px;
    object-fit: contain;
}

.nav-item{
    font-size: 1.1rem;
    font-family: var(--font-medium);
    padding:0 10px;
}

</style>