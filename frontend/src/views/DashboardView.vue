<template>
    <ManagerDashboard />
</template>

<script>
import AdminDashboard from '../components/admin/AdminDashboard.vue';
import ManagerDashboard from '../components/manager/ManagerDashboard.vue';
import UserDashboard from '../components/user/UserDashboard.vue';  
export default {
    components: {
        AdminDashboard,
        ManagerDashboard,
        UserDashboard
    },
    data() {
        return {
            userSession: JSON.parse(localStorage.getItem("userSession")) || null,
            
        };
    },
}
</script>