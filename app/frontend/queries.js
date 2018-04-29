import gql from "graphql-tag";

const venuesQuery = gql`
{
  venues {
    name
    address
    latitude
    longitude
  }
}`

module.exports = {
  venuesQuery
}
