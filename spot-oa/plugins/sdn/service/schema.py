from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField
)

from queries import MutationType

SDNSchema = GraphQLSchema(
  query=GraphQLObjectType(
    name='SDNQueryApiType',
    fields={
        'sdn': GraphQLField(
        type=MutationType,
        description='SDN API data types',
        resolver=lambda *_: {}
        )
    }
  ),
  mutation=GraphQLObjectType(
    name='SDNMutationApiType',
    fields={
      'sdn': GraphQLField(
        type=MutationType,
        description='SDN API data types',
        resolver=lambda *_: {}
      )
    }
  )
)
