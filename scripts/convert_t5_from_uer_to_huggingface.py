import argparse
import collections
import torch


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input_model_path", type=str, default="models/input_model.bin",
                    help=".")
parser.add_argument("--output_model_path", type=str, default="models/output_model.bin",
                    help=".")
parser.add_argument("--layers_num", type=int, default=12, help=".")
parser.add_argument("--decoder_layers_num", type=int, default=12, help=".")
parser.add_argument("--type", choices=["t5", "t5-v1_1"], default="t5",
                    help="The version of the t5 model.")

args = parser.parse_args()

input_model = torch.load(args.input_model_path)

output_model = collections.OrderedDict()

output_model["shared.weight"] = \
    input_model["embedding.word.embedding.weight"]

output_model["encoder.block.0.layer.0.SelfAttention.relative_attention_bias.weight"] = \
    input_model["encoder.relative_pos_emb.relative_attention_bias.weight"]
output_model["decoder.block.0.layer.0.SelfAttention.relative_attention_bias.weight"] = \
    input_model["decoder.self_pos_emb.relative_attention_bias.weight"]
output_model["encoder.embed_tokens.weight"] = \
    input_model["embedding.word.embedding.weight"]
output_model["decoder.embed_tokens.weight"] = \
    input_model["tgt_embedding.word.embedding.weight"]
output_model["lm_head.weight"] = \
    input_model["target.lm.output_layer.weight"]

for i in range(args.layers_num):
    output_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.0.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.0.SelfAttention.q.weight"]
    output_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.1.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.0.SelfAttention.k.weight"]
    output_model["encoder.transformer." + str(i) + ".self_attn.linear_layers.2.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.0.SelfAttention.v.weight"]
    output_model["encoder.transformer." + str(i) + ".self_attn.final_linear.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.0.SelfAttention.o.weight"]
    output_model["encoder.transformer." + str(i) + ".layer_norm_1.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.0.layer_norm.weight"]

    if args.type == "t5-v1_1":
        output_model["encoder.transformer." + str(i) + ".feed_forward.linear_gate.weight"] = \
            input_model["encoder.block." + str(i) + ".layer.1.DenseReluDense.wi_0.weight"]
        output_model["encoder.transformer." + str(i) + ".feed_forward.linear_1.weight"] = \
            input_model["encoder.block." + str(i) + ".layer.1.DenseReluDense.wi_1.weight"]
        output_model["encoder.transformer." + str(i) + ".feed_forward.linear_2.weight"] = \
            input_model["encoder.block." + str(i) + ".layer.1.DenseReluDense.wo.weight"]
    else:
        output_model["encoder.transformer." + str(i) + ".feed_forward.linear_1.weight"] = \
            input_model["encoder.block." + str(i) + ".layer.1.DenseReluDense.wi.weight"]
        output_model["encoder.transformer." + str(i) + ".feed_forward.linear_2.weight"] = \
            input_model["encoder.block." + str(i) + ".layer.1.DenseReluDense.wo.weight"]
    output_model["encoder.transformer." + str(i) + ".layer_norm_2.weight"] = \
        input_model["encoder.block." + str(i) + ".layer.1.layer_norm.weight"]

for i in range(args.decoder_layers_num):
    output_model["decoder.transformer_decoder." + str(i) + ".self_attn.linear_layers.0.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.0.SelfAttention.q.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".self_attn.linear_layers.1.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.0.SelfAttention.k.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".self_attn.linear_layers.2.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.0.SelfAttention.v.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".self_attn.final_linear.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.0.SelfAttention.o.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".layer_norm_1.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.0.layer_norm.weight"]

    output_model["decoder.transformer_decoder." + str(i) + ".context_attn.linear_layers.0.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.1.EncDecAttention.q.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".context_attn.linear_layers.1.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.1.EncDecAttention.k.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".context_attn.linear_layers.2.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.1.EncDecAttention.v.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".context_attn.final_linear.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.1.EncDecAttention.o.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".layer_norm_2.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.1.layer_norm.weight"]

    if args.type == "t5-v1_1":
        output_model["decoder.transformer_decoder." + str(i) + ".feed_forward.linear_gate.weight"] = \
            input_model["decoder.block." + str(i) + ".layer.2.DenseReluDense.wi_0.weight"]
        output_model["decoder.transformer_decoder." + str(i) + ".feed_forward.linear_1.weight"] = \
            input_model["decoder.block." + str(i) + ".layer.2.DenseReluDense.wi_1.weight"]
        output_model["decoder.transformer_decoder." + str(i) + ".feed_forward.linear_2.weight"] = \
            input_model["decoder.block." + str(i) + ".layer.2.DenseReluDense.wo.weight"]
    else:
        output_model["decoder.transformer_decoder." + str(i) + ".feed_forward.linear_1.weight"] = \
            input_model["decoder.block." + str(i) + ".layer.2.DenseReluDense.wi.weight"]
        output_model["decoder.transformer_decoder." + str(i) + ".feed_forward.linear_2.weight"] = \
            input_model["decoder.block." + str(i) + ".layer.2.DenseReluDense.wo.weight"]
    output_model["decoder.transformer_decoder." + str(i) + ".layer_norm_3.weight"] = \
        input_model["decoder.block." + str(i) + ".layer.2.layer_norm.weight"]

output_model["encoder.final_layer_norm.weight"] = \
    input_model["encoder.layer_norm.weight"]
output_model["decoder.final_layer_norm.weight"] = \
    input_model["decoder.layer_norm.weight"]

torch.save(output_model, args.output_model_path)
