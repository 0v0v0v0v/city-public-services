import { defineStore } from 'pinia'

import api from '../api/client'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    username: localStorage.getItem('admin_username') || '',
  }),
  getters: {
    isLoggedIn: (state) => Boolean(state.token),
  },
  actions: {
    async login(payload) {
      const { data } = await api.post('/admin/auth/login', payload)
      this.token = data.access_token
      this.username = data.username
      localStorage.setItem('admin_token', data.access_token)
      localStorage.setItem('admin_username', data.username)
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_username')
    },
  },
})
