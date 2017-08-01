from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField
)

from queries import MutationType

SdnSchema = GraphQLSchema(
  query=GraphQLObjectType(
    name='SdnQueryApiType',
    fields={
        'sdn': GraphQLField(
        type=MutationType,
        description='SDN is a security orchestration platform for the software-defined data center.',
        resolver=lambda *_: {}
        )
    }
  ),
  mutation=GraphQLObjectType(
    name='SdnMutationApiType',
    fields={
      'sdn': GraphQLField(
        type=MutationType,
        description='SDN is a security orchestration platform for the software-defined data center.',
        resolver=lambda *_: {}
      )
    }
  )
)
