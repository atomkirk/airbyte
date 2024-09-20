/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */
package io.airbyte.integrations.destination.e2e_test

import com.fasterxml.jackson.databind.JsonNode
import io.airbyte.cdk.integrations.standardtest.destination.DestinationAcceptanceTest
import io.airbyte.commons.json.Jsons
import io.airbyte.integrations.destination.e2e_test.TestingDestinations.TestDestinationType
import io.airbyte.protocol.models.v0.*
import java.util.*
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Disabled
import org.junit.jupiter.api.Test

class TestingSilentDestinationAcceptanceTest : DestinationAcceptanceTest() {
    override fun getImageName(): String {
        return "airbyte/destination-e2e-test:dev"
    }

    override fun getConfig(): JsonNode {
        return Jsons.jsonNode(
            Collections.singletonMap(
                "test_destination",
                Collections.singletonMap("test_destination_type", TestDestinationType.SILENT.name)
            )
        )
    }

    override fun getFailCheckConfig(): JsonNode {
        return Jsons.jsonNode(
            Collections.singletonMap(
                "test_destination",
                Collections.singletonMap("test_destination_type", "invalid")
            )
        )
    }

    override fun retrieveRecords(
        testEnv: TestDestinationEnv?,
        streamName: String?,
        namespace: String?,
        streamSchema: JsonNode?
    ): List<JsonNode> {
        return emptyList()
    }

    override fun setup(testEnv: TestDestinationEnv, TEST_SCHEMAS: HashSet<String>) {
        // do nothing
    }

    override fun tearDown(testEnv: TestDestinationEnv) {
        // do nothing
    }

    override fun assertSameMessages(
        expected: List<AirbyteMessage>,
        actual: List<AirbyteRecordMessage>,
        pruneAirbyteInternalFields: Boolean
    ) {
        Assertions.assertEquals(0, actual.size)
    }

    // Skip because `retrieveRecords` returns an empty list at all times.
    @Disabled @Test override fun testSyncNotFailsWithNewFields() {}

    // This test assumes that dedup support means normalization support.
    // Override it to do nothing.
    @Disabled
    @Test
    @Throws(Exception::class)
    override fun testIncrementalDedupeSync() {
        super.testIncrementalDedupeSync()
    }
}