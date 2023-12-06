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
}
</script>