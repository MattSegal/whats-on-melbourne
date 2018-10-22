module.exports = {
  event: {
    list: () =>
      fetch('/api/event/', { credentials: 'include' }),
  },
  venue: {
    list: () =>
      fetch('/api/venue/', { credentials: 'include' }),
  },
};
