const filters = {
  ADD_FILTER: (state, action) => ({
    ...state,
    filters: {
      ...state.filters,
      // Add the filtered value if it's not present already
      [action.filterType]: (state.filters[action.filterType].includes(action.value) ?
        state.filters[action.filterType] :
        [...state.filters[action.filterType], action.value]
      ),
    },
  }),
  REMOVE_FILTER: (state, action) => ({
    ...state,
    filters: {
      ...state.filters,
      // Remove the filtered value
      [action.filterType]: state.filters[action.filterType].filter(v => v !== action.value),
    },
  }),
};


const selections = {
  CLEAR_VENUE: (state, action) => ({
    ...state,
    activeVenue: null
  }),
  SET_VENUE: (state, action) => ({
    ...state,
    activeVenue: action.venue,
  }),
  OPEN_TOOLBAR: (state, action) => ({
    ...state,
    toolbarOpen: action.selected,
  }),
  CLOSE_TOOLBAR:(state, action) => ({
    ...state,
    toolbarOpen: null
  }),
}


const requests = {
  // Upsert (update or insert) a data item based on id
  // eg. To update/insert a campaign, then action.key = 'campaign')
  UPSERT_ITEM: (state, action) => ({
    ...state,
    data: {
      ...state.data,
      [action.key]: {
        ...state.data[action.key],
        loading: action.loading || false,
        lookup: { ...state.data[action.key].lookup, [action.item.id]: action.item },
        list: isItemInList(action.item, state.data[action.key].list) ?
          updateItemInList(action.item, state.data[action.key].list) :
          addItemToList(action.item, state.data[action.key].list),
      },
    },
  }),
  // Mark a set of data items as "loading"
  SET_LOADING: (state, action) => ({
    ...state,
    data: {
      ...state.data,
      [action.key]: {
        ...state.data[action.key],
        loading: true,
      },
    },
  }),
  UNSET_LOADING: (state, action) => ({
    ...state,
    data: {
      ...state.data,
      [action.key]: {
        ...state.data[action.key],
        loading: false,
      },
    },
  }),
  // Received a set of data items from the backend
  RECEIVE_LIST: (state, action) => ({
    ...state,
    data: {
      ...state.data,
      [action.key]: {
        isCached: true,
        loading: false,
        list: action.data,
        lookup: action.data.reduce((obj, el) => { obj[el.id] = el; return obj; }, {}),
      },
    },
  }),
  RESET_CACHE: state => ({
    ...state,
    data: Object.entries(state.data)
      .reduce((stateData, [key, data]) => ({
        ...stateData,
        [key]: {
          ...data,
          isCached: false,
        },
      }), {}),
  }),
}


const reducers = {
  ...filters,
  ...selections,
  ...requests,
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
