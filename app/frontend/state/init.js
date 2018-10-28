
// initial state for the app
const dataDefault = { loading: true, isCached: false, lookup: {}, list: [] };

module.exports = {
  data: {
    // Data items - this is all sourced from the backend
    venue: { ...dataDefault },
    event: { ...dataDefault },
  },
  filters: {
    GENRE: [],
  },
  selected: {
    // Items selected by the user
    venue: null,
    toolbar: null,
  },
};
