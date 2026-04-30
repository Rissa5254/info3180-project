<template>
    <div class="search-container">
        <h3>Browse Potential Matches</h3>
        <div class="filters">
             <!-----Search----->
            <input v-model="filters.q" placeholder="Search by name or bio..." />

             <!------Age Range------>
            <select v-model="filters.ageRange">
                <option value="">All Ages</option>
                <option value="18-25">18-25</option>
                <option value="26-35">26-35</option>
                <option value="36-50">36-50</option>
                <option value="51+">51+</option>
            </select>

             <!----Location---->
            <input v-model="filters.location" placeholder="Filter by location..." />           
        </div>

         <!---Buttons-->
        <button @click="ShowInterests"> Show Interest Filters</button> <br />
        <button @click="Reset"> Reset Filters</button>

        <!---Results-->
        <div class="results">
            <div v-for="user in users" :key="user.id" class="user-card">
                <h4>{ user.name }</h4>
                <p>{ user.bio }</p>
                <p>Age: { user.age }</p>
            </div>
        </div>
    </div>
    
</template>

<script>
export default{
    data(){
        return{
            filters:{
                q: "",
                ageRange:"",
                location:""
            },
            users: [],
            ShowInterests: false
        };
    },
};
</script>

<style scoped>
.search-container{
    background: #f5f5f5;
    padding: 20px;
}
.filters{
    display: flex;
    gap: 25px;
    margin-bottom: 10px; 
    margin-top: 15px;
}

.filters input, select, button{
    width: 100%;
    border: none;
    border-radius: 5px;
    padding: 5px;
}

button{
    margin-bottom: 10px;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
}

button:first-of-type{
    background-color: rgb(68, 68, 236);
}

button:last-of-type{
    background-color: rgb(163, 159, 159);
}
</style>