<template lang="pug">
  v-col(cols="12")
    VueFileAgent(
      ref="actPhotos"
      :value="actPhotos"
      @input="actPhotos = $event"
      theme="list"
      :accept="'.png, .jpeg, .jpg'"
      :maxSize="'10MB'"
      :maxFiles="5"
      :multiple="true"
      :deletable="true"
      :helpText="'Загрузите свой файл'"
      :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 10MB' }"
      @delete="fileDeleted($event)"
    )
    small *Файл должен быть с расширением .png, .jpeg, .jpg и размером меньше 10 мегабайт
</template>

<script>
export default {
  computed: {
    actPhotos: {
      set (actPhotos) {
        this.$store.commit('act/SET_ACT', { photos: actPhotos })
      },
      get () {
        return this.$store.state.act.detail.photos
      }
    }
  },
  methods: {
    fileDeleted (fileRecord) {
      const i = this.actPhotos.indexOf(fileRecord)
      if (i !== -1) {
        this.actPhotos = this.actPhotos.splice(i, 1)
      }
    }
  }
}
</script>
