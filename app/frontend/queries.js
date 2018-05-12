import gql from "graphql-tag";

const venuesQuery = gql`
{
  venues {
    name
    address
    latitude
    longitude
    website
    events {
      name
      artist
      price
      eventType
      startsAt
    }
  }
}`

module.exports = {
  venuesQuery
}
