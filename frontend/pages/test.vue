<template lang="pug">
  div
    VueSuggestions(
      :model.sync="city"
      :coordinates.sync="coordinates"
      :placeholder="'Начните вводить'"
      :options="suggestionOptions"
      class="form-control"
    )
</template>

<script>
import VueSuggestions from 'vue-suggestions'

export default {
  components: { VueSuggestions },
  data: () => ({
    city: 'Новокузнецк',
    coordinates: {
      latitude: '',
      longitude: ''
    },
    suggestionOptions: {
      // @see https://confluence.hflabs.ru/pages/viewpage.action?pageId=207454318
      token: '519fbd1afac8c2380f617046c95a6789a39fa021',
      type: 'ADDRESS',
      scrollOnFocus: false,
      triggerSelectOnBlur: false,
      triggerSelectOnEnter: false,
      addon: 'none',
      // @see https://confluence.hflabs.ru/pages/viewpage.action?pageId=207454320
      onSelect (suggestion) {}
    }
  })
}
</script>
