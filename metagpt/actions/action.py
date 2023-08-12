#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : action.py
"""
from abc import ABC
from typing import Optional

from openai.error import APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, wait_fixed, after_log, retry_if_exception_type
from tiktoken import Encoding

from metagpt.actions.action_output import ActionOutput
from metagpt.llm import LLM
from metagpt.utils.common import OutputParser
from metagpt.logs import logger

import tiktoken

class Action(ABC):
    def __init__(self, name: str = '', context=None, llm: LLM = None):
        self.name: str = name
        if llm is None:
            llm = LLM()
        self.llm = llm
        self.context = context
        self.prefix = ""
        self.profile = ""
        self.desc = ""
        self.content = ""
        self.instruct_content = None

    def set_prefix(self, prefix, profile):
        """Set prefix for later usage"""
        self.prefix = prefix
        self.profile = profile

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    async def _aask(self, prompt: str, system_msgs: Optional[list[str]] = None) -> str:
        """Append default prefix"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)

        return await self._call_llm_aask(prompt, system_msgs)

    async def _aask_no_prefix(self, prompt: str, system_msgs: list[str]) -> str:
        """Append default prefix"""
        return await self._call_llm_aask(prompt, system_msgs)


    async def _aask_v1(self, prompt: str, output_class_name: str,
                       output_data_mapping: dict,
                       system_msgs: Optional[list[str]] = None) -> ActionOutput:
        """Append default prefix"""
        if not system_msgs:
            system_msgs = []
        system_msgs.append(self.prefix)
        content = await self._call_llm_aask(prompt, system_msgs)
        logger.debug(content)
        output_class = ActionOutput.create_model_class(output_class_name, output_data_mapping)
        parsed_data = OutputParser.parse_data_with_mapping(content, output_data_mapping)
        logger.debug(parsed_data)
        instruct_content = output_class(**parsed_data)
        return ActionOutput(content, instruct_content)


    def tokens_count(self, enc: Encoding, prompt: str, system_msgs: list[str]) -> int:
        strNewLine = '\n'
        allText = f'''
            
            {strNewLine.join(system_msgs)}
            
            {prompt}
            
            '''
        tokens = enc.encode(allText, allowed_special='all')
        return len(tokens)


#    @retry(stop=stop_after_attempt(10), wait=wait_exponential_jitter(initial=1))
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        after=after_log(logger, logger.level('WARNING').name),
        retry=retry_if_exception_type(APIConnectionError),
        #retry_error_callback=log_and_reraise,
    )
    async def _call_llm_aask(self, prompt: str, system_msgs: list[str]) -> str:
        enc = tiktoken.encoding_for_model("gpt-4")
        while self.tokens_count(enc, prompt, system_msgs) > 8000-3000:
            system_msgs = system_msgs[1:]

        strNewLine = '\n'
        strAll = f'''
{strNewLine.join(system_msgs)}

{prompt}
'''
        text_len = len(strAll)
        logger.info(f'''

00000000000000000000000000000000

_call_llm_aask len: {text_len}

system_msgs:
{strNewLine.join(system_msgs)}

prompt:
{prompt}

00000000000000000000000000000000

''')
        return await self.llm.aask(prompt, system_msgs)


    async def run(self, *args, **kwargs):
        """Run action"""
        raise NotImplementedError("The run method should be implemented in a subclass.")
