export const types = {
    SET_CONTRAGENTS: 'SET_CONTRAGENTS',
    FETCH_CONTRAGENTS: 'FETCH_CONTRAGENTS',

    SET_CONTRAGENT: 'SET_CONTRAGENT',
    FETCH_CONTRAGENT: 'FETCH_CONTRAGENT'
}

export const state = () => ({
    list: [],
    detail: {}
})

export const mutations = {
    [types.SET_CONTRAGENT] (state, contragent) {
        state.detail = contragent
    },
    [types.SET_CONTRAGENTS] (state, contragents) {
        state.list = contragents
    }
}

export const actions = {
    // add (state, text) {
    //     state.list.push({
    //         text,
    //         done: false
    //     })
    // },
    // remove (state, { todo }) {
    //     state.list.splice(state.list.indexOf(todo), 1)
    // },
    async [types.FETCH_CONTRAGENT] (store, id) {
        const data = await this.$axios.$get(`http://localhost/api/contragent/${id}`)
        store.commit(types.SET_CONTRAGENT, data)
    },
    async [types.FETCH_CONTRAGENTS] (store) {
        const data = await this.$axios.$get('http://localhost/api/contragents/')
        store.commit(types.SET_CONTRAGENTS, data)
    }
}

export const getters = {
    // loadedPosts (state) {
    //     return state.loadedPosts
    // }
}
