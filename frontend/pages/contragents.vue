<template lang="pug">
    v-row(
        class="fill-height"
        justify="center"
        align="start"
        no-gutters
    )
        v-col(
            class="fill-height"
            xs12
            sm8
            md6
        )
            v-card(
                class="fill-height"
                flat
                exact
            )
                v-card-text(class="pa-0")
                    v-data-table(
                        :headers="headers"
                        :items="contragents"
                        class="elevation-0"
                        disable-sort
                        disable-pagination
                        disable-filtering
                        calculate-widths
                    )
                        template(v-slot:top)
                            v-toolbar(flat)
                                v-toolbar-title Контрагенты
                                v-spacer
                                v-btn(outlined class="mt-2 text-capitalize" color="primary" @click="contragentDialogState = true") Добавить контрагента
                        template(v-slot:body="{ items }")
                            tbody
                                router-link(tag="tr" :to="'contragent/' + item.id" v-for="item in items" :key="item.name")
                                    td {{ item.excell_name }}
                                    td {{ item.physical_address }}
                                    td {{ item.klass }}
                                    td {{ item.inn }}
                                    td {{ item.debt }}
            v-dialog(v-model="contragentDialogState" persistent max-width="600px")
                v-card(outlined)
                    v-card-title
                        span(class="headline") Добавление контрагента
                    v-card-text
                        v-container(px-0 pb-0)
                            v-row(no-gutters)
                                v-col(cols="12")
                                    VueFileAgent(
                                        class="profile-pic-upload-block"
                                        ref="profilePicRef"
                                        v-model="profilePic"
                                        :theme="'list'"
                                        :accept="'.xlsx'"
                                        :maxSize="'2MB'"
                                        :maxFiles="1"
                                        :multiple="false"
                                        :deletable="true"
                                        :compact="true"
                                        :helpText="'Загрузите свой файл'"
                                        :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                                        @select="onSelect($event)"
                                    )
                                    small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
                    v-card-actions
                        v-spacer
                        v-btn(color="blue darken-1" text @click="contragentDialogState = false") Закрыть
                        v-btn(color="blue darken-1" text @click="upload") Отправить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/contragents.js'

// const classTypes = [
//     { 0: '' },
//     { 1: 'Юридическое лицо без договора' },
//     { 2: 'Юридическое лицо с договором' },
//     { 3: 'ИЖС без договора' },
//     { 4: 'ИЖС с договором' },
//     { 5: 'Физическое лицо' }
// ]

export default {
    async asyncData ({ $axios, store, params }) {
        await store.dispatch(`contragents/${types.FETCH_CONTRAGENTS}`)
    },
    data: () => ({
        uploaded: false,
        uploadHeaders: {},
        profilePic: null,
        uploadUrl: 'http://localhost/api/contragents/',
        contragentDialogState: false,
        headers: [
            {
                text: 'Название',
                align: 'left',
                sortable: false,
                value: 'excell_name'
            },
            { text: 'Факт. адрес', value: 'physical_address' },
            {
                text: 'Класс',
                value: 'klass'
            },
            { text: 'ИНН', value: 'inn' },
            { text: 'Задолжность', value: 'debt' }
            // Дата последнего платежа
            // Ответственное лицо
        ]
    }),
    computed: {
        ...mapState({
            contragents: state => state.contragents.list
        })
    },
    methods: {
        ...mapActions([types.FETCH_CONTRAGENTS]),
        removePic () {
            const profilePic = this.profilePic
            this.$refs.profilePicRef.deleteUpload(this.uploadUrl, this.uploadHeaders, [profilePic])
            this.profilePic = null
            this.uploaded = false
        },
        upload () {
            const self = this
            this.$refs.profilePicRef.upload(this.uploadUrl, this.uploadHeaders, [this.profilePic]).then(function () {
                self.uploaded = true
                setTimeout(function () {
                // self.profilePic.progress(0);
                }, 500)
            })
        },
        onSelect (filesData) {
            this.uploaded = false
        }
    }
}
</script>
