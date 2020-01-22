<template lang="pug">
    v-row(
        class="fill-height"
        justify="center"
        align="start"
        no-gutters
    )
        v-col(
            xs12
            sm8
            md6
        )
            v-card(
                flat
                exact
            )
                v-card-title(class="headline font-weight-light px-10")
                    | Контрагент № {{ contragent.id }}
                v-card-text
                    v-expansion-panels(
                        v-model="panels"
                        accordion
                        multiple
                        hover
                        flat
                        tile
                    )
                        v-expansion-panel(
                            v-for="(item, i) in contragentInfo"
                            :key="i"
                        )
                            v-expansion-panel-header {{ Object.keys(item)[0] }}
                            v-expansion-panel-content
                                //- v-subheader {{ item.name }}
                                v-text-field(v-if="Object.values(item)" :label="Object.values(item)[0]")
                                //- v-row(v-if="item.items")
                                //-     v-col(
                                //-         v-for="(date, i) in item.items"
                                //-         :key="i"
                                //-         cols="6"
                                //-     )
                                //-         v-subheader(class="pa-0 ma-0") {{ date.title }}
                                //-         v-text-field(:label="date.value")
                v-card-actions(class="px-10 py-6")
                    v-spacer
                    v-btn(
                        color="primary"
                        nuxt
                        to="/inspire"
                    )
                        | Сохранить
</template>

<script>
import { mapState } from 'vuex'
import { types } from '~/store/contragents.js'

export default {
    async asyncData ({ $axios, store, params }) {
        await store.dispatch(`contragents/${types.FETCH_CONTRAGENT}`, params.id)
    },
    data: () => ({
        test: 'qwe'
        // contragent: [
        //     {
        //         title: 'Тип контрагента',
        //         name: 'Новоселова Наталья Александровна',
        //         address: 'Россия, Кемеровская область, Киселёвск, улица Поповича, 5'
        //     },
        //     {
        //         title: 'Физическое лицо',
        //         id: 113313,
        //         name: 'Новоселова Наталья Александровна',
        //         phone: '+7 908 957-62-88'
        //     },
        //     {
        //         title: 'Информация',
        //         items: [
        //             {
        //                 title: 'Дата создания',
        //                 value: '2019-12-30'
        //             },
        //             {
        //                 title: 'Дата изменения',
        //                 value: '2019-12-30'
        //             }
        //         ]
        //     }
        // ]
    }),
    computed: {
        ...mapState({
            contragentInfo: (state) => {
                const data = state.contragents.detail
                const result = Object.keys(data).map((key) => {
                    const test = {}
                    test[key] = `${data[key]}`
                    return test
                })
                return result
            },
            contragent: state => state.contragents.detail
        }),
        panels () {
            return [...Array(this.contragentInfo.length).keys()]
        }
    },
    methods: {}
}
</script>
