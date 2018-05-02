import gql from "graphql-tag";

const venuesQuery = gql`
{
  venues {
    name
    address
    latitude
    longitude
    events {
      name
      artist
      price
      startsAt
    }
  }
}`

module.exports = {
  venuesQuery
}
